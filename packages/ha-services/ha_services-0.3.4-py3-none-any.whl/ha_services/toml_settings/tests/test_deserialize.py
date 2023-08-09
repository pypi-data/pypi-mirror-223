import dataclasses
import inspect
import logging
from pathlib import Path
from unittest import TestCase

import tomlkit

from ha_services.cli_tools.test_utils.environment_fixtures import AsSudoCallOverrideEnviron
from ha_services.toml_settings.deserialize import toml2dataclass
from ha_services.toml_settings.tests.fixtures import ComplexExample, PathExample, SimpleExample


class DeserializeTestCase(TestCase):
    def test_toml2dataclass_simple(self):
        instance = SimpleExample()
        data = dataclasses.asdict(instance)
        self.assertEqual(data, {'one': 'foo', 'two': 'bar', 'three': '', 'number': 123})

        document = tomlkit.loads(
            inspect.cleandoc(
                '''
                # Own Comment,
                # should be keep
                two = "New Value"
                three = 666 # Wrong type!
                number = 123 # Contains the same value!

                [other]
                foo = "bar"
                '''
            ),
        )
        with self.assertLogs(logger=None, level=logging.DEBUG) as logs:
            toml2dataclass(document=document, instance=instance)
        print('\n'.join(logs.output))

        data = dataclasses.asdict(instance)
        self.assertEqual(
            data,
            {
                'one': 'foo',
                'two': 'New Value',  # <<< changed
                'three': '',
                'number': 123,
            },
        )
        toml = tomlkit.dumps(document)
        self.assertEqual(
            toml,
            inspect.cleandoc(
                '''
                # Own Comment,
                # should be keep
                two = "New Value"
                three = "" # Wrong type!
                number = 123 # Contains the same value!
                one = "foo"

                [other]
                foo = "bar"
                '''
            ),
        )

        self.assertEqual(
            logs.output,
            [
                "INFO:ha_services.toml_settings.deserialize:Missing 'one' in toml config",
                #
                "INFO:ha_services.toml_settings.deserialize:Take over 'two' from user toml setting",
                #
                'ERROR:ha_services.toml_settings.deserialize:Toml value three=666 is type '
                "'int' but must be type 'str' -> ignored and use default value!",
                #
                'DEBUG:ha_services.toml_settings.deserialize:Default value 123 also used in toml file, ok.',
            ],
        )

    def test_toml2dataclass_path(self):
        instance = PathExample()
        data = dataclasses.asdict(instance)
        self.assertEqual(
            data,
            {
                'path': Path('/foo/bar'),
            },
        )

        document = tomlkit.loads(
            inspect.cleandoc(
                '''
                path = "/to/some/other/place/"
                '''
            ),
        )

        toml2dataclass(document=document, instance=instance)

        data = dataclasses.asdict(instance)
        self.assertEqual(
            data,
            {
                'path': Path('/to/some/other/place'),
            },
        )

        # Path entries can use "~":
        real_home = Path().home()
        toml2dataclass(document=tomlkit.loads('path = "~/foo/"'), instance=instance)
        self.assertEqual(instance.path, real_home / 'foo')

        # sudo calls will be also use the user home and not /root/

        with AsSudoCallOverrideEnviron():
            self.assertEqual(Path('~').expanduser(), Path('/root'))
            toml2dataclass(document=tomlkit.loads('path = "~/bar/"'), instance=instance)
            self.assertEqual(instance.path, real_home / 'bar')

    def test_toml2dataclass_inheritance(self):
        instance = ComplexExample()
        data = dataclasses.asdict(instance)
        self.assertEqual(
            data,
            {
                'foo': 'bar',
                'sub_class_one': {'number': 123},
                'sub_class_two': {'something': 0.5},
                'sub_class_three': {'one_value': True},
            },
        )

        document = tomlkit.loads(
            inspect.cleandoc(
                '''
                [sub_class_one]
                number = "Not a Number!"

                [sub_class_two]
                something = 123.456
                '''
            ),
        )
        with self.assertLogs(logger=None, level=logging.DEBUG) as logs:
            toml2dataclass(document=document, instance=instance)
        print('\n'.join(logs.output))

        data = dataclasses.asdict(instance)
        self.assertEqual(
            data,
            {
                'foo': 'bar',  # <<< not change, because not in toml file
                'sub_class_one': {
                    'number': 123,  # <<< not change, because wrong type
                },
                'sub_class_two': {
                    'something': 123.456,  # <<< updated
                },
                'sub_class_three': {'one_value': True},  # <<< added
            },
        )
        toml = tomlkit.dumps(document).rstrip()
        self.assertEqual(
            toml,
            inspect.cleandoc(
                '''
                foo = "bar"
                [sub_class_one]
                number = 123

                [sub_class_two]
                something = 123.456
                [sub_class_three]
                # SubClass3(one_value: bool = True)
                one_value = true
                '''
            ),
        )

        self.assertEqual(
            logs.output,
            [
                "INFO:ha_services.toml_settings.deserialize:Missing 'foo' in toml config",
                #
                "ERROR:ha_services.toml_settings.deserialize:Toml value number='Not a "
                "Number!' is type 'str' but must be type 'int' -> ignored and use default "
                'value!',
                #
                "INFO:ha_services.toml_settings.deserialize:Take over 'something' from user toml setting",
                #
                'INFO:ha_services.toml_settings.deserialize:Missing complete sub dataclass '
                "'sub_class_three' in toml config",
            ],
        )
