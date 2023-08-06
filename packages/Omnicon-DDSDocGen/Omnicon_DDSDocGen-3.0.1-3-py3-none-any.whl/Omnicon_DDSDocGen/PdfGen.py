import os
import sys
import logging
from . import Logger
import docx2pdf
# due to https://stackoverflow.com/questions/74787311/error-with-docx2pdf-after-compiling-using-pyinstaller
# logger = Logger.add_logger("__name__")
# sys.stderr = Logger.LoggerFakeWriter(logger.error)
# sys.stderr = Logger.LoggerWriter(logger.error)


from .DocxGen import DocxGen
import pythoncom

class PdfGen(DocxGen):
    def __init__(self, title: str, new_version: str,  time: str, origin_version: str = "",
                        origin_dds_types_files: list = None,
                        new_dds_types_files: list = None,
                        origin_dds_topics_types_mapping: str = "",
                        new_dds_topics_types_mapping: str = ""):
        """
        This class allows creating one of two documents; an ICD (created by docGen) and a comparison document (created
        by DocCompare). The difference is in the title page; the version in the ICD is added on its on, but in the
        comparison document both versions are displayed in a table along with the files/folders used by each version

        IMPORTANT:
        WHEN origin_version COMES EMPTY , WE KNOW IT'S AN ICD, and new_version IS USED AS THE VERSION.
        WHEN origin_version IS NOT EMPTY, WE KNOW IT'S A COMPARISON DOCUMENT.

        """
        super().__init__(title=title,
                         new_version=new_version,
                         time=time,
                         origin_version=origin_version,
                         origin_dds_types_files=origin_dds_types_files,
                         new_dds_types_files=new_dds_types_files,
                         origin_dds_topics_types_mapping=origin_dds_topics_types_mapping,
                         new_dds_topics_types_mapping=new_dds_topics_types_mapping)
        self.logger = Logger.add_logger(__name__)

    def generate_doc(self, output_file_name: str, temp_folder: str)->str:
        # TODO if there is an issue while using at UI then revert the following 2 lines
        logger = Logger.add_logger("__name__")
        sys.stderr = Logger.LoggerFakeWriter(logger.error)

        self.logger.debug(self.generate_doc.__name__)
        # Create the docx using DocxGen
        super().generate_doc(output_file_name, temp_folder)

        temp_docx_file_name = f'{output_file_name}.docx'
        temp_docx_path = os.path.join(temp_folder, temp_docx_file_name)
        temp_pdf_file_name = f'{output_file_name}.pdf'
        temp_pdf_path = os.path.join(temp_folder, temp_pdf_file_name)

        # Convert to PDF and save into the requested folder
        try:
            self.logger.debug(f"saving {temp_pdf_file_name} into {temp_folder}")
            # keep_active is to prevent the 'docx2pdf.convert' from closing the docx that might be open:
            pythoncom.CoInitialize()
            docx2pdf.convert(temp_docx_path, temp_pdf_path, keep_active=True)

            self.logger.info(f"File saved successfully into '{temp_pdf_path}'")

        except Exception as err:

            self.logger.error(f"Could not save '{temp_pdf_path}'.", exc_info=True)

        sys.stderr = Logger.LoggerWriter(logger.error)

