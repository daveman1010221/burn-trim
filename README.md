# burn-trim

Three crates of [burn](https://github.com/tracel-ai/burn) and [cubecl](https://github.com/tracel-ai/cubecl), as
published to crates.io, with the backends Polar never builds taken out of their manifests. Polar builds burn for
Vulkan (wgpu) only; burn's other backends bring build-time downloaders (libtorch through `burn-tch` and `torch-sys`,
LLVM through `cubecl-cpu` and `tracel-llvm-bundler`) that fetch over TLS with a store of roots no one in Polar chose.
Cargo records every optional dependency in `Cargo.lock`, built or not, so they appeared in Polar's lock although nothing
compiled them.

Polar takes these crates with `[patch.crates-io]`, pinned by revision.

| Crate | Version | crates.io checksum (sha256 of the `.crate`) |
|---|---|---|
| cubecl | 0.11.4 | 7d44bb3fb8559ef4e7e107df09df37b7f5a5a7d45ab063148a0d25c1cdd13990 |
| burn-dispatch | 0.22.1 | 64d255d7609901f7aaf2138b394a6fe8dd8c7b526d1ed2736ba2c643944028fa |
| burn-signal | 0.22.1 | 3afcc7d0f8654ccf9529c9e93f21383b8828d4c784c0429966d2026698f72451 |

The first commit is each crate exactly as its `.crate` file holds it; the trim follows, and its diff is the whole
change: the manifests, and the two files cargo writes when it packages a crate (`Cargo.toml.orig`,
`.cargo_vcs_info.json`), which it refuses to find in a git dependency's source when Nix vendors it. Features are kept, emptied where they named a removed backend, so every crate that names them still resolves.

The code is burn's and cubecl's, under their licence: MIT or Apache-2.0, at your option.
