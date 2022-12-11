from cortex import Cortex
import pyautogui
import math


class Emotiv():

    def __init__(self, client_id, client_secret, **kwargs):
        self.c = Cortex(client_id, client_secret, debug_mode=False, **kwargs)
        
        self.c.bind(create_session_done=self.on_session_start)
        self.c.bind(new_mot_data=self.on_new_data)
        self.c.bind(inform_error=self.on_error)


    def start(self, data, device_id=''):
        self.data = data

        if device_id != '':
            self.c.set_wanted_headset(device_id)

        self.c.open()


    def on_session_start(self, *args, **kwargs):
        self.c.sub_request(self.data)


    def on_new_data(self, *args, **kwargs):
        new_data = kwargs.get('data')

        q0 = new_data['mot'][2]
        q1 = new_data['mot'][3]
        q2 = new_data['mot'][4]
        q3 = new_data['mot'][5]
        
        roll = math.atan2(2*(q0*q1 + q2*q3), 1 - 2*(q1*q1 + q2*q2))
        pitch = math.asin(2*(q0*q2 - q3*q1))
        yaw = math.atan2(2*(q0*q3 + q1*q2), 1 - 2*(q2*q2 + q3*q3))
        
        roll = int(roll*180/math.pi)
        pitch = int(pitch*180/math.pi)
        yaw = int(yaw*180/math.pi)

        if abs(roll) > 90:
            pyautogui.move(-2, 0, _pause=False)
        else:
            pyautogui.move(2, 0, _pause=False)

        if abs(pitch) > 60:
            pyautogui.move(0, -2, _pause=False)
        else:
            pyautogui.move(0, 2, _pause=False)


    def on_error(self, *args, **kwargs):
        error_data = kwargs.get('error_data')
        print(error_data)


def main():

    client_id = ''
    client_secret = ''

    emotiv = Emotiv(client_id, client_secret)

    data_labels = ['mot']
    emotiv.start(data_labels)

if __name__ =='__main__':
    main()
