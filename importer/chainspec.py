import json


class ChainSpecGenerator:
    """
    Import state via chainspec constructs
    """

    def __init__(self, target_spec_path, state_export):
        with open(target_spec_path) as f:
            self.target_spec = json.load(f)
        with open(state_export) as f:
            self.state_export = json.load(f)['state']
            # we need to change balance from hex to decimal representation
            for _, _state in self.state_export.items():
                _state["balance"] = str(int(_state["balance"], 16))
                _state["nonce"] = str(int(_state["nonce"], 16))

    def generate_spec(self, output_path):
        """
        Enriches state from existing chain with target chain spec
        :param output_path:
        :return:
        """
        self.target_spec['accounts'].update(self.state_export)
        with open(output_path, 'w') as f:
            json.dump(self.target_spec, f, indent=4)

