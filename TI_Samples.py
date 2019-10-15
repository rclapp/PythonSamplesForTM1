from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def Send_Data_TM1_TI(tm1, file, param1, param2):
    '''
    :param tm1: Connection to a TM1 Service
    :param file: File to load
    :param param1: TI Parameter 1
    :param param2: TI Parameter 2
    :return: Success (Bool)
    '''

    load_data_ti = 'Sample Load Data From File Process'
    file = Path(file)

    try:
        success, status, error_log_file = tm1.processes.execute_with_return(load_data_ti,
                                                                            pParam1=param1,
                                                                            pParam2=param2,
                                                                            pFile=str(file.resolve()))

        if success:
            target = 'Complete'
        else:
            target = 'Error'

        logger.info(f'Load Process {target} {file}')

        target_path = file.parent / f'{target}/'

        #rename file
        new_file_name = f'{file.stem}_{target}_{settings.time_stamp}{file.suffix}'
        new_file_name_and_new_path = target_path / new_file_name

        file.rename(new_file_name_and_new_path)

        logger.debug(f'Moved file {file} to {new_file_name_and_new_path}')

        #get TM1 Error file and add it to error directory
        if error_log_file is not None:
            error_file_content = tm1.processes.get_error_log_file_content(error_log_file)
            new_error_file_name = new_file_name_and_new_path.with_suffix('.log')
            with new_error_file_name.open(mode='w') as csv:
                csv.write(error_file_content)

        return success

    except Exception as e:
        logger.exception('Send Data via TI Failed',exc_info=True)


