# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spline_agent',
 'spline_agent.commons',
 'spline_agent.commons.configuration',
 'spline_agent.decorators',
 'spline_agent.dispatchers']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.2.0,<4.0.0',
 'http-constants>=0.5.0,<0.6.0',
 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'spline-agent',
    'version': '0.1.0',
    'description': 'Spline agent for Python. Lineage tracking utility.',
    'long_description': '# Spline agent for Python scripts [PoC]\n\nSee: https://github.com/AbsaOSS/spline\n\nThe goal is to create a module that would act as a wrapper around a user Python code,\nthat would execute it in a lineage trackable manner. The main idea is that the user would create a function,\ne.g. `my_awesome_function`, that accepts input and output data source definitions as function arguments,\nand it would execute some logic reading the data from input sources, transforming it in some way and writing\nthe result into the output. Then, in order to track lineage, the user would decorate that function with the \nSpline Python agent decorators and execute the function as usual.\nThe Agent would then intercept the call, inspect the given function and the input/output definitions,\nexecute the function, take some stats, create a lineage metadata and send it to the Spline server in a similar way\nthe [Spark Agent](https://github.com/AbsaOSS/spline-spark-agent) does it.\nSo that the lineage tracking process would be as seamless and non-intrusive to the user code as possible in Python.\n\n### Example\n\n```python\nimport spline_agent\nfrom spline_agent.enums import WriteMode\n\n\n# Decorate a function you want to track with as follows\n@spline_agent.track_lineage()\n@spline_agent.inputs(\'{input_source_1}\', \'{input_source_2}\')\n@spline_agent.output(\'{output_source}\', WriteMode.APPEND)\ndef my_awesome_function(output_source, input_source_1, input_source_2):\n    print("read from input source")\n    print("do some business logic")\n    print("write into the output")\n\n\n# Execute the target function as normal\nmy_awesome_function("some_url_1", "some_url_2", "some_url_3")\n```\n\nThe `inputs()` and `output()` decorators could be places on any other\nfunction that is called (also transitively) from the `my_awesome_function`.\nThe data source can be represented as a URL string t the source,\nor the string containing the Spline Expression (SpEL) - currently ir only\nsupports the format `"{func_parameter_name}"` (e.r. `"{abc}"` would mean -\ntake the value from the `abc` parameter of the decorated function).\n\n# Building\n\n### TL;DR\n\n```shell\nmake build install\n```\n\n### Makefile targets\n\n- _Default_ - Runs tests and linters.\n- `clean` - Remove output directory (`dist`)\n- `build` - Full clean build with everything excepts for installing.\n- `install` - Install WHEEL file produced by the `build` target\n\n---\n\n    Copyright 2023 ABSA Group Limited\n\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n',
    'author': 'Oleksandr Vayda',
    'author_email': 'oleksandr.vayda@absa.africa',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AbsaOSS/spline-python-agent',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
