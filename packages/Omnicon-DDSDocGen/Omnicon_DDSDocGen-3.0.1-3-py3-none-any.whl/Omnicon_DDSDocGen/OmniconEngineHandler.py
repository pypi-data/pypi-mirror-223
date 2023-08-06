from . import Logger
from Omnicon_GenericDDSEngine_Py import Omnicon_GenericDDSEngine_Py as Omnicon


class OmniconEngineHandler:
    def __init__(self, input_files_and_dirs_list: list):

        self.logger = Logger.add_logger(__name__)
        self.engine = None
        self.init_and_run_engine(input_files_and_dirs_list)


    def init_and_run_engine(self, input_files_and_dirs_list: list) -> Omnicon.GenericDDSEngine:
        """
        This creates an engine instance and performs init and run with the desired configurations.
        :param input_files_and_dirs_list: A string that holds the path of the folder that holds the input_pointer files
        """
        # Create an engine instance:
        self.engine = Omnicon.GenericDDSEngine()
        try:
            factory_configuration = Omnicon.FactoryConfiguration()
            factory_configuration.loggerConfiguration.verbosity = Omnicon.LogSeverityLevel.info
            Omnicon.GenericDDSEngine.SetFactoryConfiguration(factory_configuration)
        except:
            pass

        # Create an engine configuration object:
        engine_configuration = Omnicon.EngineConfiguration()
        # Set the parameters:
        engine_configuration.threadPoolSize = 3
        # Go over the new list and append it into the configuration file path vector:
        for input_file in input_files_and_dirs_list:
            engine_configuration.ddsConfigurationFilesPath.append(input_file)
        # Perform the introspection:
        engine_configuration.engineOperationMode = \
            Omnicon.EngineOperationMode.TYPE_INTROSPECTION
        # init the engine:
        self.logger.debug("init engine...")

        self.engine.Init(engine_configuration)
        self.logger.info("Engine was init successfully")
        # Run the engine:
        self.engine.Run()
        # When Init() went well, make a log entry:
        self.logger.debug("Engine is now up and running")

    def shutdown_engine(self):
        try:
            self.logger.debug("Shutting down Omnicon engine")
            if self.engine:
                self.engine.Shutdown()
                del self.engine
                self.engine = None
            self.logger.debug("Engine shutdown is complete")
        except Exception as error:
            self.logger.error("shutdown_introspection_engine exception occurred:", error)
