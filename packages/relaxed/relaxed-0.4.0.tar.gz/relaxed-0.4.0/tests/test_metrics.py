from __future__ import annotations

import jax.numpy as jnp
import numpy as np
import pytest
from dummy_pyhf import example_model
from jax import jacrev, tree_map
from jax.random import PRNGKey

import relaxed


@pytest.fixture()
def data():
    nBg = 8000
    nSig = 300
    bins = np.linspace(0, 70, 10)
    background = np.histogram(np.random.normal(40, 10, nBg), bins=bins)[0]
    signal = np.histogram(np.random.normal(50, 5, nSig), bins=bins)[0]
    return signal, background


def test_gaussianity():
    model = example_model(5.0, n_bins=2)
    pars = {"mu": jnp.array(0.0), "shapesys": jnp.array([1.0, 1.0])}
    data = model.expected_data(pars)
    relaxed.metrics.gaussianity(model, pars, data, PRNGKey(0))


def test_gaussianity_grad():
    def pipeline(x):
        model = example_model(5.0, n_bins=2)
        pars = {"mu": jnp.array(0.0), "shapesys": jnp.array([1.0, 1.0])}
        data = model.expected_data(pars)
        return relaxed.metrics.gaussianity(
            model,
            tree_map(lambda a: a * x, pars),
            (data[0] * x, data[1] * x),
            PRNGKey(0),
        )

    jacrev(pipeline)(4.0)  # just check you can calc it w/o exception


def test_significance(data):
    signal, background = data

    def one_bin_significance(S, B):
        return jnp.sqrt(2 * ((S + B) * jnp.log(1 + S / B) - S))

    # non-zero signal bin
    assert np.allclose(
        one_bin_significance(signal[6], background[6]),
        relaxed.metrics.asimov_sig(signal[6], background[6]),
    )

    relaxed.metrics.asimov_sig(signal, background)


def test_significance_grad(data):
    def pipeline(
        pars, bw, endpoints  # bin widths up to the last one (determined by endpoints)
    ):
        s, b = data
        start, end = endpoints
        bins = jnp.cumsum(jnp.array([start, *pars, (end - start) - jnp.sum(pars)]))
        sig_hist = relaxed.hist(s, bins=bins, bandwidth=bw)
        bg_hist = relaxed.hist(b, bins=bins, bandwidth=bw)
        return relaxed.metrics.asimov_sig(sig_hist, bg_hist)

    jacrev(pipeline)(
        jnp.array([5.0, 10.0, 15.0]), 1e-3, (0, 70)
    )  # just check you can calc it w/o exception
