from call_controler import CallController
from config.server import SERVER_URL, MIC_PORT, SPEAKER_PORT, USER_ID

if __name__ == '__main__':
    call_controller = CallController(
        url=SERVER_URL,
        mic_port=MIC_PORT,
        speaker_port=SPEAKER_PORT,
        user_id=USER_ID
    )
