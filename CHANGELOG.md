# Changelog

## [1.1.0](https://github.com/andrelair-platform/minicloud-agent/compare/minicloud-agent-v1.0.1...minicloud-agent-v1.1.0) (2026-09-04)


### Features

* **ci:** add dev branch build — tags dev-&lt;sha&gt;, updates dev gitops overlay ([8ece8f6](https://github.com/andrelair-platform/minicloud-agent/commit/8ece8f63fb53c0a026b7ec1dc50f3a48779efb3a))
* initial service extraction from minicloud-gitops ([fc1c038](https://github.com/andrelair-platform/minicloud-agent/commit/fc1c038917a87b6f09b14be0b0719cfbfb1cc0d8))


### Bug Fixes

* **ci:** direct PR merge (auto-merge disabled on minicloud-gitops) ([33031bb](https://github.com/andrelair-platform/minicloud-agent/commit/33031bb2cc8d978b9ac511d6d722f8775d536565))
* **ci:** GPG-sign gitops commit and use PR flow (main branch is protected) ([d3a20e5](https://github.com/andrelair-platform/minicloud-agent/commit/d3a20e52efad8986d5dd1aa0b161f09343b6d773))
* **ci:** restart Docker daemon after CA cert injection for buildx ([52b6d45](https://github.com/andrelair-platform/minicloud-agent/commit/52b6d45420dd835df9c25c90d8ec520fc2e0e36e))
* **ci:** use buildkitd insecure=true for Harbor (buildx container can't see host CA) ([6071b13](https://github.com/andrelair-platform/minicloud-agent/commit/6071b13508920e02e6b1dd016ca98de2e7341815))
* **lint:** sort imports, drop isort rule (code not isort-authored) ([85b34c6](https://github.com/andrelair-platform/minicloud-agent/commit/85b34c60cfe464b46c5cff2797bd50855030c79d))
* **tests:** correct patch target and exclude AI-only files from coverage ([58fa167](https://github.com/andrelair-platform/minicloud-agent/commit/58fa167240d22417223f7a63c21a0583f8fa640e))

## Changelog

All notable changes to minicloud-agent are documented here.

This file is maintained by [release-please](https://github.com/googleapis/release-please).
