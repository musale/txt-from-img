.PHONY: build
build:
	@cd layers && ./build.sh

.PHONY: package_layers
package_layers:
	@ cd layers && serverless package

.PHONY: deploy_layers
deploy_layers:
	@ cd layers && serverless deploy

.PHONY: build_serverless
build_serverless:
	@yarn install

.PHONY: zip
zip:
	@zip -9qyr txt-from-img.zip . -x

.PHONY: lint
lint:
	@pipenv run black functions tests

.PHONY: tests
tests:
	@pipenv run pytest -v