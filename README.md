# Fee-based Transaction Order Encoding

## Environment

```bash
export ORDER_HOME=$HOME/Documents/orderencode
export PYTHON_HOME=$HOME/Virtualenvs/PyOrder
export PYTHONPATH=$ORDER_HOME
export ORDER_DATA_PATH=$HOME/Data/ordering
export CHAIN_RIDER_TOKEN=
```

## Initialization

```bash
pyvenv-3.5 $PYTHON_HOME
source $PYTHON_HOME/bin/activate
pip install -r resources/requirementx.txt
```

## Dash block data downloads

```bash
curl https://api.chainrider.io/v1/dash/main/block/00000000000000230eb73bf1a63f4f024c6fa9b12af0c3e9e4bf726889183697?token=<token> \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json' > template
```
