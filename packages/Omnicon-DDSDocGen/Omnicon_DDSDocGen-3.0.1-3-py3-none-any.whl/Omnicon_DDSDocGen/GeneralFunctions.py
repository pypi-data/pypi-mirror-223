import enum
import inspect
import os
import types
import hashlib
import traceback

from .DocxGen import DocxGen


def check_artifacts_integrity(logger):
    logger.debug("check_artifacts_integrity")
    # print(get_hash_of_template())
    if not get_hash_of_template() == '7d6d8c09b081bfe18fbae885f53967e5':
        logger.fatal("DocGen resource 'Template.Docx' was modified. Cannot start DocGen.")
        raise Exception("FATAL: DocGen resource 'Template.Docx' was modified. Cannot start DocGen.")


def get_hash_of_template(verbose=0):
    SHAhash = hashlib.md5()

    template_file = DocxGen.get_doc_template_path()
    if not os.path.exists(template_file):
        return -1

    try:
        if verbose == 1:
            print('Hashing file')
        # filepath = os.path.join(os.getcwd(), file_name)
        with open(template_file, 'rb') as f1:
            while 1:
                # Read file in as little chunks
                buf = f1.read()
                # remove carriage returns due to different file saving methods
                buf = buf.replace(b'\r', b'')
                if not buf:
                    break
                SHAhash.update(buf)

    except:
        # Print the stack traceback
        raise (traceback.print_exc())
    return SHAhash.hexdigest()


def check_input_types(origin_input_files_and_dirs_list: list,
                      origin_topic_names_to_types_xml_path: str,
                      output_file_name: str,
                      title: str,
                      origin_version: str,
                      new_version: str,
                      output_folder: str,
                      output_formats: list,
                      new_input_files_and_dirs_list: list,
                      new_topic_names_to_types_xml_path: str,
                      is_ignore_id: bool = False):
    if type(origin_input_files_and_dirs_list) != list:
        error_message: str = f"Invalid input! Parameter <input_files_and_dirs_list>: '{origin_input_files_and_dirs_list}' " \
                             f"is: {type(origin_input_files_and_dirs_list)}. Should be of class 'list'."
        raise Exception(error_message)

    if type(new_input_files_and_dirs_list) != list:
        error_message: str = f"Invalid input! Parameter <input_files_and_dirs_list>: '{new_input_files_and_dirs_list}' " \
                             f"is: {type(new_input_files_and_dirs_list)}. Should be of class 'list'."
        raise Exception(error_message)

    if type(origin_topic_names_to_types_xml_path) != str:
        error_message: str = f"Invalid input! Parameter <topic_names_to_types_xml_path>: " \
                             f"'{origin_topic_names_to_types_xml_path}' is: " \
                             f"{type(origin_topic_names_to_types_xml_path)}. Should be of class 'string'."
        raise Exception(error_message)

    if type(new_topic_names_to_types_xml_path) != str:
        error_message: str = f"Invalid input! Parameter <topic_names_to_types_xml_path>: " \
                             f"'{new_topic_names_to_types_xml_path}' is: " \
                             f"{type(new_topic_names_to_types_xml_path)}. Should be of class 'string'."
        raise Exception(error_message)

    if type(output_file_name) != str:
        error_message: str = f"Invalid input! Parameter Parameter <output_file_name>: '{output_file_name}' is: " \
                             f"{type(output_file_name)}. Should be of class 'string'."
        raise Exception(error_message)

    if type(title) != str:
        error_message: str = f"Invalid input! Parameter <title>: '{title}' is: " \
                             f"{type(title)}. Should be of class 'string'."
        raise Exception(error_message)

    if type(origin_version) != str:
        error_message: str = f"Invalid input! Parameter <origin_version> '{origin_version}' is: " \
                             f"{type(origin_version)}. Should be of class 'string'."
        raise Exception(error_message)
    if type(new_version) != str:
        error_message: str = f"Invalid input! Parameter <new_version> '{new_version}' is: " \
                             f"{type(new_version)}. Should be of class 'string'."
        raise Exception(error_message)

    if type(output_folder) != str:
        error_message: str = f"Invalid input! Parameter <output_folder> '{output_folder}' is: " \
                             f"{type(output_folder)}. Should be of class 'string'."
        raise Exception(error_message)

    if type(output_formats) != list:
        error_message: str = f"Invalid input! Parameter <output_formats> '{output_formats}' is: " \
                             f"{type(output_formats)}. Should be of class 'list'."
        raise Exception(error_message)

    if type(is_ignore_id) != bool:
        error_message: str = f"Invalid input! Parameter <is_ignore_id>: '{is_ignore_id}' is: " \
                             f"{type(is_ignore_id)}. Should be of class 'list'."
        raise Exception(error_message)


def check_output_format_list(output_format_list):
    error_message: str
    example_message: str = "Please add a list of requested formats. For example: ['pdf']. " \
                           "Another example: ['docx', 'pdf']."
    if output_format_list is None:
        error_message = f"Invalid input! Parameter <output_format> is 'None'. {example_message}"
        raise Exception(error_message)
    if len(output_format_list) == 0:
        error_message = f"Invalid input! Parameter <output_format> is an empty list.{example_message}"
        raise Exception(error_message)


def check_path(output_folder: str):
    # Check folder validity
    if not os.path.exists(os.path.join(os.getcwd(), output_folder)):
        error_message = f"Selected output folder '{os.path.join(os.getcwd(), output_folder)}' does not exist. " \
                        f"Please create the folder or choose an existing one."
        raise Exception(error_message)

    # Preparing an error message in advance
    error_message = f"Fatal: Cannot write into selected output folder '{os.path.join(os.getcwd(), output_folder)}'. " \
                    f"Please check writing permissions and try again."
    # Check writing permissions:
    if not os.access(os.path.join(os.getcwd(), output_folder), os.W_OK):
        raise Exception(error_message)

    # Sometimes os.access may return True even if the app does not have write permissions. So the following section
    # will try to create a temporary file into output_folder then immediately remove it.
    # If there are no write permissions then an exception will be raised.
    try:
        testfile = os.path.join(os.path.join(os.getcwd(), output_folder), 'temp.txt')
        with open(testfile, 'w') as f:
            f.write('test')
        os.remove(testfile)

    except OSError:
        raise Exception(error_message)


def check_type_files_not_empty(input_files_and_dirs_list: list):
    # Check if the list is empty
    if input_files_and_dirs_list is None:
        error_message = f"input_files_and_dirs_list is None. Cannot create an ICD without type file(s) or" \
                        f" a folder that contains at least one."
        raise Exception(error_message)


def check_progress_callback_function_signature(progress_callback_function):
    if progress_callback_function is not None:
        if not isinstance(progress_callback_function, types.FunctionType):
            error_message: str = f"Invalid input! Parameter <progress_callback_function> " \
                                 f"'{progress_callback_function}' is: " \
                                 f"{type(progress_callback_function)}. Should be of class 'function'."
            raise Exception(error_message)

    # define an allowed signature with 3 parameters
    if progress_callback_function is not None:

        # get the signature of OF
        signature = inspect.signature(progress_callback_function)
        num_params = len(signature.parameters)
        # compare the signatures
        if num_params != 3:
            raise Exception("The provided progress_bar_function has an invalid signature. "
                            "Please check README.md for progress bar function")


def check_input(origin_input_files_and_dirs_list: list,
                origin_topic_names_to_types_xml_path: str,
                output_file_name: str,
                title: str,
                origin_version: str,
                new_version: str,
                output_folder: str,
                output_formats: list,
                new_input_files_and_dirs_list: list = None,
                new_topic_names_to_types_xml_path: str = os.getcwd(),
                is_ignore_id: bool = False):
    """
    This function checks several aspects of the input. IF there is an issue, an exception is thrown.
    """
    # Allow this function to work even when it is called by docgen (without the parameters that has the prefix 'new')
    if not new_input_files_and_dirs_list:
        new_input_files_and_dirs_list = [""]

    check_input_types(
        origin_input_files_and_dirs_list=origin_input_files_and_dirs_list,
        origin_topic_names_to_types_xml_path=origin_topic_names_to_types_xml_path,
        output_file_name=output_file_name,
        title=title,
        origin_version=origin_version,
        new_version=new_version,
        output_folder=output_folder,
        output_formats=output_formats,
        new_input_files_and_dirs_list=new_input_files_and_dirs_list,
        new_topic_names_to_types_xml_path=new_topic_names_to_types_xml_path,
        is_ignore_id=is_ignore_id)

    check_output_format_list(output_formats)

    # check if output folder even exists
    check_path(output_folder)  # SEE NOTE BElOW
    # NOTE: Since there is a list of requested type files, we check (for each type file) if the output file
    # is open at a later stage, when calling that type file's docGen's init method (for example, in the case
    # of a PDF, the test happens in LatexDocGen.__init__)

    check_type_files_not_empty(origin_input_files_and_dirs_list)
    check_type_files_not_empty(new_input_files_and_dirs_list)


def get_type_name(DDS_type):
    """
    This function is used by the sort() function; The returned value is used as a key for sorting alphabetically
    :param DDS_type: An element from the list received from GetTypesBasicInfo,
    :return:
    """
    return DDS_type.fullName


def order_topics_by_xml(topic_names_to_types_xml: str, alphabet_order_list: list, ET=None):
    """
    This function returns a list of topic
    :param ET:
    :param topic_names_to_types_xml:
    :param alphabet_order_list:
    :return:
    """
    topic_mapping_dict: dict = {}
    tree = ET.parse(topic_names_to_types_xml)
    root = tree.getroot()
    for topic in root.findall('domain_library/domain/topic'):
        topic_name = topic.get('name')
        dds_type = topic.get('register_type_ref')
        if topic_name in alphabet_order_list:
            topic_mapping_dict[topic_name] = dds_type

    return topic_mapping_dict


class PhaseEnum(enum.IntEnum):
    PARSE_ORIGIN_PHASE = 0
    PARSE_REVISED_PHASE = 1
    COMPARE_PHASE = 2
    WRITE_RESULTS_PHASE = 3
    SAVE_RESULTS_PHASE = 4
