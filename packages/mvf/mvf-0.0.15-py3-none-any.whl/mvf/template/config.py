import yaml
import os


class ConfigBuilder:
    '''
    Writes a template config file for an MVF project.
    If a file already exists, user changes will not be overwritten.
    '''
    config = {
        'data': {
            'source': 'path_to_your_source_code',
            'lang': 'Python',
            'split': 'train_test',
            'test_size': 0.3,
            'input_features': [],
            'target_features': []
        },
        'models': [
            {
                'name': 'your_model_name',
                'lang': 'Python',
            },
        ],
    }

    def __init__(self, pth):
        '''
        Initialises the builder with template config.
        Updates with any existing config.

        Needs to be refactored. This method should not be creating
        a directory. This should be handled by mvf.cli.init
        '''
        # make project dir if not already exists
        if not os.path.exists(pth):
            os.makedirs(pth)
        # construct path to config file
        self.config_path = os.path.join(
            pth,
            'mvf_conf.yaml',
        )
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                existing_config = yaml.safe_load(f)
            self.config.update(existing_config)

    def write(self):
        '''
        Writes config to file.
        '''
        with open(self.config_path, 'w') as f:
            yaml.safe_dump(self.config, f, default_flow_style=False)
