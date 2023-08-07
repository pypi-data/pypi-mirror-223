# GailBot

## About

Researchers studying human interaction, such as conversation analysts, psychologists, and linguists all rely on detailed transcriptions of language use. Ideally, these should include so-called paralinguistic features of talk, such as overlaps, prosody, and intonation, as they convey important information. However, transcribing these features by hand requires substantial amounts of time by trained transcribers. There are currently no Speech to Text (STT) systems that are able to annotate these features. To reduce the resources needed to create transcripts that include paralinguistic features, we developed a program called GailBot. GailBot combines STT services with plugins to automatically generate first drafts of conversation analytic transcripts. It also enables researchers to add new plugins to transcribe additional features, or to improve the plugins it currently uses. We argue that despite its limitations, GailBot represents a substantial improvement over existing dialogue transcription software.

Find the full paper published by Dialogue and Discourse [here](https://journals.uic.edu/ojs/index.php/dad/article/view/11392).


## Status

GailBot version: 0.1a11 (Pre-release)
Release type: API


## Installation

GailBot and the necessary dependencies can be installed using pip with the following commands:
```
    pip install --upgrade pip

    pip install gailbot
    pip install git+https://github.com/linto-ai/whisper-timestamped
    pip install git+https://github.com/m-bain/whisperx.git
```


## Usage - GailBot API

This release features a convenient API to use GailBot and create custom plugin suites. To use the API and its features, import the GailBot package like the following:

```
    from gailbot import GailBot
```

Once you have imported the GailBot package, initialize an instance of GailBot called "gb" (or a name of your choosing) by doing the following ("ws_root" is takes a path to your workspace directory):

```
    gb = GailBot(ws_root="your_workspace_path")
```
The GailBot API's methods are now available through your GailBot instance. Check out GailBot's backend documentation for a full list of method and their uses [here](https://gailbot-release-document.s3.us-east-2.amazonaws.com/Documentation/Backend_Technical_Documentation.pdf).


### Example Usage - Default Settings




Now, we will try to use the GailBot to transcribe some input audio files. To do so, we will need to set up a new profile, add input source files, register and apply plugin suite, and finally transcribe. See the example below:
```
    settings_dictionary = {
        "core": {},
        "plugins": {
            "plugins_to_apply": ["demoPlugin"]
        },
        "engines": {
            "engine_type": "watson",
            "watson_engine": {
                "watson_api_key": WATSON_API_KEY,
                "watson_language_customization_id": WATSON_LANG_CUSTOM_ID,
                "watson_base_language_model": WATSON_BASE_LANG_MODEL,
                "watson_region": WATSON_REGION,

            }
        }
    }

    gb.create_new_setting("demo_profile", settings_dictionary)
    gb.add_source(
        source_path="your_source_file_path"
        output_dir="your_output_directory_path"
    )
    gb.register_plugin_suite("path_to_test_plugin_suite")
    gb.apply_setting_to_source(
        "your_source_file_path", 
        "demo_profile"
    )
    gb.transcribe()
```
In the above example, we first create a dictionary with key-value pairs that are required to create a GailBotSettings object. Note that "plugins_to_apply" is a list of plugin names that will be applied for that specific settings profile. Since GailBot currently supports IBM Watson STT, users must first create an [IBM Bluemix account](https://cloud.ibm.com/registration?target=catalog%3fcategory=watson&cm_mmc=Earned-_-Watson+Core+-+Platform-_-WW_WW-_-intercom&cm_mmca1=000000OF&cm_mmca2=10000409&). Next, a watson api key and region must be created with [IBM](https://cloud.ibm.com/catalog/services/speech-to-text) and specified in the settings profile.

With the settings dictionary specified, we create a new profile called "demo_profile" with the values defined in the settings dictionary. 

Next, we add input source files by specifying the paths to their directories.

Then, register a plugin suite into your GailBot instance.
Finally, apply the profile setting you've set up ("demo_profile") to your source input
and begin transcribing.


## Supported Plugin Suites

A core GailBot feature is its ability to apply plugin suites during the transcription process. While different use cases may require custom plugins, the Human Interaction Lab maintains and distributes a pre-developed custom suite -- HiLabSuite.


### HiLabSuite

This is the main plugin suite that is maintained by the Human Interaction Lab. It uses a multi-layered approach to generate a list structure storing transcription results, supports multiple data views (word level, utterance level etc.), and produces output in various formats.

The following demonstrates how HiLabSuite may be used with GailBot:

```
    HILABSUITE_PLUGINS = [
        "hilab",
        "OutputFileManager",
        "SyllableRatePlugin",
        "GapPlugin",
        "PausePlugin",
        "OverlapPlugin",
        "CSVPlugin",
        "TextPlugin",
        "XmlPlugin",
        "ChatPlugin"
    ]

    settings_dict = {
        "core": {},
        "plugins": {
            "plugins_to_apply": HILABSUITE_PLUGINS
        },
        "engines": {
            "engine_type": "watson",
            "watson_engine": {
                "watson_api_key": WATSON_API_KEY,
                 "watson_language_customization_id": "",
                "watson_base_language_model": WATSON_BASE_LANG_MODEL,
                "watson_region": WATSON_REGION,

            }
        }
    }

    gb = GailBot(ws_root="your_workspace_path")
    plugin_suite_paths

    gb.create_new_setting("demo_profile", settings_dict)

    gb.register_plugin_suite("path_to_HiLabSuite")

    gb.add_source(
        source_path="your_source_file_path"
        output_dir="your_output_directory_path"
    )

    gb.apply_setting_to_source(
        "your_source_file_path", 
        "demo_profile"
    )

    gb.transcribe()

```
In the above code, we initialize GailBot, create a new settings profile that applies plugins for the HILabPlugin suite, add a source to transcribe, and produce results by applying the plugin suite.

Note that in the get_settings_dict() method, users will have to enter their custom WATSON_API_KEY, WATSON_REGION, and WATSON_BASE_LANG_MODEL. These are generated from the [IBM Watson](https://cloud.ibm.com/login) service.

### Custom Plugins

A core GailBot feature is its ability to allow researchers to develop and add custom plugins that may be applied during the transcription process, in addition to the provided built-in HiLabSuite.


## Contribute

Users are encouraged to direct installation and usage questions, provide feedback, details regarding bugs, and development ideas by [email](mailto:hilab-dev@elist.tufts.edu).


## Acknowledgements

Special thanks to members of the [Human Interaction Lab](https://sites.tufts.edu/hilab/) at Tufts University and interns that have worked on this project.


## Cite

Users are encouraged to cite GailBot using the following BibTex:
```
@article{umair2022gailbot,
  title={GailBot: An automatic transcription system for Conversation Analysis},
  author={Umair, Muhammad and Mertens, Julia Beret and Albert, Saul and de Ruiter, Jan P},
  journal={Dialogue \& Discourse},
  volume={13},
  number={1},
  pages={63--95},
  year={2022}
}
```

## Liability Notice

Gailbot is a tool to be used to generate specialized transcripts. However, it
is not responsible for output quality. Generated transcripts are meant to
be first drafts that can be manually improved. They are not meant to replace
manual transcription.

GailBot may use external Speech-to-Text systems or third-party services. The
development team is not responsible for any transactions between users and these
services. Additionally, the development team does not guarantee the accuracy or 
correctness of any plugin. Plugins have been developed in good faith and we hope 
that they are accurate. However, users should always verify results.

By using GailBot, users agree to cite Gailbot and the Tufts Human Interaction Lab
in any publications or results as a direct or indirect result of using Gailbot.