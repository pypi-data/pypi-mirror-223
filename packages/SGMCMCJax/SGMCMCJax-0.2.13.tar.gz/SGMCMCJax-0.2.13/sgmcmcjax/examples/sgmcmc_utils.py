# Various extensions to https://github.com/jeremiecoullon/SGMCMCJax
# Author : Kevin Murphy(@murphyk), Aleyna Kara(@karalleyna)

# copied from https://github.com/probml/pyprobml/blob/master/scripts/sgmcmc_utils.py

import jax
import jax.numpy as jnp
import optax
from blackjax import nuts, stan_warmup
from jax import jit, lax, random, tree_leaves, tree_map, vmap
from jax.random import split

from sgmcmcjax.gradient_estimation import build_gradient_estimation_fn
from sgmcmcjax.util import build_grad_log_post, progress_bar_scan

# Extends https://github.com/jeremiecoullon/SGMCMCJax/blob/master/sgmcmcjax/samplers.py
# by making a wrapper for blackjax.nuts (https://github.com/blackjax-devs/blackjax),
# so it acts like other sgmcmc samplers (ie takes loglikelihood and logprior, instead of potential)


def inference_loop(rng_key, kernel, initial_state, num_samples, pbar):
    def one_step(carry, i):
        state, key = carry
        kernel_key, key = split(key)
        state, _ = kernel(kernel_key, state)
        return (state, key), state

    lebody = progress_bar_scan(num_samples)(one_step) if pbar else one_step
    _, states = lax.scan(lebody, (initial_state, rng_key), jnp.arange(num_samples))
    return states


def build_log_post(loglikelihood, logprior, data):
    if len(data) == 1:
        batch_loglik = jit(vmap(loglikelihood, in_axes=(None, 0)))
    elif len(data) == 2:
        batch_loglik = jit(vmap(loglikelihood, in_axes=(None, 0, 0)))
    else:
        raise ValueError("Data must be a tuple of size 1 or 2")

    def log_post(params):
        return logprior(params) + jnp.sum(batch_loglik(params, *data), axis=0)

    return jit(log_post)


def build_nuts_sampler(
    num_warmup, loglikelihood, logprior, data, batchsize=None, pbar=True
):
    # wrapper for blackjax, so it acts like other sgmcmc samplers
    log_post = build_log_post(loglikelihood, logprior, data)

    def potential(params):
        v = log_post(params)
        return -v

    def nuts_sampler(rng_key, num_samples, initial_params):
        initial_state = nuts.new_state(initial_params, potential)

        kernel_generator = lambda step_size, inverse_mass_matrix: jit(
            nuts.kernel(potential, step_size, inverse_mass_matrix)
        )
        stan_key, key = split(rng_key)

        final_state, (step_size, inverse_mass_matrix), _ = stan_warmup.run(
            stan_key, kernel_generator, initial_state, num_warmup
        )

        nuts_kernel = kernel_generator(step_size, inverse_mass_matrix)

        inference_key, key = split(key)
        states = inference_loop(
            inference_key, nuts_kernel, final_state, num_samples, pbar
        )
        return states.position

    return nuts_sampler
