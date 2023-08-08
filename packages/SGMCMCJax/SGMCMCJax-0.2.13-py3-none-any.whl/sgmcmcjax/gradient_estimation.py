from collections import namedtuple
from typing import Any, Callable, Tuple

import jax.numpy as jnp
from jax import jit, lax, random
from jax.tree_util import tree_flatten, tree_map, tree_unflatten

from .types import PRNGKey, PyTree, SamplerState, SVRGState


# standard gradient estimator
def build_gradient_estimation_fn(
    grad_log_post: Callable, data: Tuple, batch_size: int
) -> Tuple[Callable, Callable]:
    """Build a standard gradient estimator

    Args:
        grad_log_post (Callable): gradient of the log-posterior
        data (Tuple): tuple of data. It should either have a single array (for unsupervised problems) or have two arrays (for supervised problems)
        batch_size (int): batch size

    Returns:
        Tuple[Callable, Callable]: gradient estimation function and gradient initialisation function
    """
    assert type(data) == tuple
    N_data, *_ = data[0].shape
    data = tuple(
        [jnp.array(elem) for elem in data]
    )  # this makes sure data has jax arrays rather than numpy arrays

    def init_gradient(key: PRNGKey, param: PyTree) -> Tuple[PyTree, SVRGState]:
        idx_batch = random.choice(key=key, a=jnp.arange(N_data), shape=(batch_size,))
        minibatch_data = tuple([elem[idx_batch] for elem in data])
        param_grad = grad_log_post(param, *minibatch_data)
        return param_grad, SVRGState()

    @jit
    def estimate_gradient(
        i: int, key: PRNGKey, param: PyTree, svrg_state: SVRGState = SVRGState()
    ) -> Tuple[PyTree, SVRGState]:
        if (batch_size is None) or batch_size == N_data:
            return grad_log_post(param, *data), svrg_state
        else:
            return init_gradient(key, param)

    return estimate_gradient, init_gradient


# Control variates
def build_gradient_estimation_fn_CV(
    grad_log_post: Callable, data: Tuple, batch_size: int, centering_value: PyTree
) -> Tuple[Callable, Callable]:
    """Build a Control Variates gradient estimator

    Args:
        grad_log_post (Callable): gradient of the log-posterior
        data (Tuple): tuple of data. It should either have a single array (for unsupervised problems) or have two arrays (for supervised problems)
        batch_size (int): batch size
        centering_value (PyTree): Centering value for the control variates (should be the MAP)

    Returns:
        Tuple[Callable, Callable]: gradient estimation function and gradient initialisation function
    """
    assert type(data) == tuple
    N_data, *_ = data[0].shape
    data = tuple(
        [jnp.array(elem) for elem in data]
    )  # this makes sure data has jax arrays rather than numpy arrays

    fb_grad_center = grad_log_post(centering_value, *data)
    flat_fb_grad_center, tree_fb_grad_center = tree_flatten(fb_grad_center)
    update_fn = lambda c, g, gc: c + g - gc

    def init_gradient(key: PRNGKey, param: PyTree):
        idx_batch = random.choice(key=key, a=jnp.arange(N_data), shape=(batch_size,))
        minibatch_data = tuple([elem[idx_batch] for elem in data])

        param_grad = grad_log_post(param, *minibatch_data)
        grad_center = grad_log_post(centering_value, *minibatch_data)
        flat_param_grad, tree_param_grad = tree_flatten(param_grad)
        flat_grad_center, tree_grad_center = tree_flatten(grad_center)
        new_flat_param_grad = tree_map(
            update_fn, flat_fb_grad_center, flat_param_grad, flat_grad_center
        )
        param_grad = tree_unflatten(tree_param_grad, new_flat_param_grad)
        return param_grad, SVRGState()

    @jit
    def estimate_gradient(
        i: int, key: PRNGKey, param: PyTree, svrg_state: SVRGState = SVRGState()
    ) -> Tuple[PyTree, SVRGState]:
        return init_gradient(key, param)

    return estimate_gradient, init_gradient


def build_gradient_estimation_fn_SVRG(
    grad_log_post: Callable, data: Tuple, batch_size: int, update_rate: int
) -> Tuple[Callable, Callable]:
    """Build a SVRG gradient estimator

    Args:
        grad_log_post (Callable): gradient of the log-posterior
        data (Tuple): tuple of data. It should either have a single array (for unsupervised problems) or have two arrays (for supervised problems)
        batch_size (int): batch size
        update_rate (int): how often to update the centering value in the gradient estimator

    Returns:
        Tuple[Callable, Callable]: gradient estimation function and gradient initialisation function
    """
    assert type(data) == tuple
    N_data, *_ = data[0].shape
    data = tuple(
        [jnp.array(elem) for elem in data]
    )  # this makes sure data has jax arrays rather than numpy arrays
    update_fn = lambda c, g, gc: c + g - gc

    def update_centering_value(param: PyTree) -> SVRGState:
        fb_grad_center = grad_log_post(param, *data)
        flat_fb_grad_center, tree_fb_grad_center = tree_flatten(fb_grad_center)
        svrg_state = SVRGState(param, flat_fb_grad_center)
        return svrg_state

    def init_gradient(key: PRNGKey, param: PyTree) -> Tuple[PyTree, SVRGState]:
        fb_grad_center = grad_log_post(param, *data)
        flat_fb_grad_center, tree_fb_grad_center = tree_flatten(fb_grad_center)
        svrg_state = SVRGState(param, flat_fb_grad_center)
        return fb_grad_center, svrg_state

    @jit
    def estimate_gradient(
        i: int, key: PRNGKey, param: PyTree, svrg_state: SVRGState
    ) -> Tuple[PyTree, SVRGState]:
        svrg_state = lax.cond(
            i % update_rate == 0,
            lambda _: update_centering_value(param),
            lambda _: svrg_state,
            None,
        )
        idx_batch = random.choice(key=key, a=jnp.arange(N_data), shape=(batch_size,))
        minibatch_data = tuple([elem[idx_batch] for elem in data])

        param_grad = grad_log_post(param, *minibatch_data)
        grad_center = grad_log_post(svrg_state.centering_value, *minibatch_data)
        flat_param_grad, tree_param_grad = tree_flatten(param_grad)
        flat_grad_center, tree_grad_center = tree_flatten(grad_center)
        new_flat_param_grad = tree_map(
            update_fn, svrg_state.fb_grad_center, flat_param_grad, flat_grad_center
        )
        param_grad = tree_unflatten(tree_param_grad, new_flat_param_grad)
        return param_grad, svrg_state

    return estimate_gradient, init_gradient
