IDRIC ?= idris2
IDRIC_REVISION ?= 081b9cde0
PYTHON ?= python3

DRIVER := build/exec/idric-wasm
MODULE := build/exec/known-integer.wasm
DETERMINISM_A := build/exec/known-integer-a.wasm
DETERMINISM_B := build/exec/known-integer-b.wasm
VENV := build/wasmtime-venv
WASMTIME_PYTHON := $(VENV)/bin/python
BACKEND_SOURCES := $(wildcard src/Backend/Wasm/*.idr) backend.ipkg

.PHONY: check-compiler check driver module shape runtime determinism verify clean

check-compiler:
	@$(IDRIC) --version | grep -q '$(IDRIC_REVISION)' || { \
		echo "Expected Idriç compiler revision $(IDRIC_REVISION)"; \
		$(IDRIC) --version; \
		exit 1; \
	}

check: check-compiler
	$(IDRIC) --typecheck backend.ipkg

driver: $(DRIVER)

$(DRIVER): $(BACKEND_SOURCES)
	$(IDRIC) --build backend.ipkg

$(MODULE): $(DRIVER) tests/KnownInteger.idric
	IDRIS2_PATH="$(CURDIR)/build/ttc:$${IDRIS2_PATH}" \
		./$(DRIVER) --cg wasm --source-dir tests tests/KnownInteger.idric -o known-integer

module: $(MODULE)

shape: $(MODULE)
	$(PYTHON) tests/check_module_shape.py $(MODULE) --export idric_answer --value 42

$(WASMTIME_PYTHON): tools/requirements-wasmtime.txt
	$(PYTHON) -m venv $(VENV)
	$(WASMTIME_PYTHON) -m pip install --disable-pip-version-check -r tools/requirements-wasmtime.txt

runtime: $(MODULE) $(WASMTIME_PYTHON)
	$(WASMTIME_PYTHON) tests/validate_and_run.py $(MODULE) --export idric_answer --expect 42

$(DETERMINISM_A): $(DRIVER) tests/KnownInteger.idric
	IDRIS2_PATH="$(CURDIR)/build/ttc:$${IDRIS2_PATH}" \
		./$(DRIVER) --cg wasm --source-dir tests tests/KnownInteger.idric -o known-integer-a

$(DETERMINISM_B): $(DRIVER) tests/KnownInteger.idric
	IDRIS2_PATH="$(CURDIR)/build/ttc:$${IDRIS2_PATH}" \
		./$(DRIVER) --cg wasm --source-dir tests tests/KnownInteger.idric -o known-integer-b

determinism: $(DETERMINISM_A) $(DETERMINISM_B)
	@cmp -s $(DETERMINISM_A) $(DETERMINISM_B) || { \
		cmp -l $(DETERMINISM_A) $(DETERMINISM_B) | head; \
		echo "Wasm bytes changed across identical compilations"; \
		exit 1; \
	}

verify: check shape determinism runtime

clean:
	rm -rf build
