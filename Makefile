setup:
	rm -rf .github
	npm install
	python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
	sed -i -e s/{{test}}/`basename $(CURDIR)`/g app.py

make-dia: synth
	mkdir -p docs/imgs
	npx cdk-dia --target docs/imgs/diagram

# CDK

integ-runner:
	export CDK_INTEG_RUNNER_CWD=$(PWD) && npx integ-runner

integ-runner-debug:
	export CDK_INTEG_RUNNER_CWD=$(PWD) && npx integ-runner --no-clean --verbose --update-on-failed

synth:
	npx cdk -a "python3 app.py" synth

deploy:
	npx cdk -a "python3 app.py" deploy

destroy:
	npx cdk -a "python3 app.py" destroy

hotswap:
	npx cdk -a "python3 app.py" deploy --hotswap
