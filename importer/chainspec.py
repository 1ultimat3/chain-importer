import json
import ijson

from importer.streamer import json_states


class ChainSpecGenerator:
    """
    Import state via chainspec constructs
    """

    def __init__(self, target_spec_path, state_export):
        self.target_spec = target_spec_path
        self.state_export = state_export

    def generate_spec(self, output_path):
        """
        Enriches state from existing chain with target chain spec
        :param output_path:
        :return:
        """
        with open(self.state_export) as state_fd:
            with open(self.target_spec) as template_fd:
                parser = ijson.parse(template_fd)
                depth_map = {}
                depth_val = -1
                with open(output_path, 'w') as out:
                    for prefix, event, value in parser:
                        if event == "string":
                            out.write("\"{1}\"".format(prefix.split('.')[-1], value))
                        elif event == "number":
                            out.write("{1}".format(prefix.split('.')[-1], value))
                        elif event == 'null':
                            out.write('null')
                        elif event == 'start_map':
                            depth_val += 1
                            depth_map[depth_val] = 0
                            out.write('{')

                            if prefix == 'accounts':
                                for _exported_state in json_states(state_fd):
                                    _address = _exported_state['address']
                                    del _exported_state['address']
                                    _json_acc = "\"{0}\": {1}".format(
                                        _address,
                                        json.dumps(_exported_state)
                                    )
                                    if depth_map[depth_val] == 0:
                                        out.write(_json_acc)
                                    else:
                                        out.write(",")
                                        out.write(_json_acc)
                                    depth_map[depth_val] = 1

                        elif event == 'map_key':
                            if depth_map[depth_val] == 0:
                                out.write('"{0}":'.format(value))
                            else:
                                out.write(',"{0}":'.format(value))
                            depth_map[depth_val] += 1
                        elif event == 'end_map':
                            depth_val -= 1
                            out.write('}')
