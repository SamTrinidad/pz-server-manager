import argparse
import os
import boto3
from dotenv import load_dotenv
# Load environment variables from the root directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
EC2_INSTANCE_ID = os.environ.get('EC2_INSTANCE_ID')

#starting instance
#tmux new -s "pz" -d
#tmux send-keys -t "pz" "cd ~/.steam/steam/SteamApps/common/Project\ Zomboid\ Dedicated\ Server/" C-m
#tmux send-keys -t "pz" "bash start-server.sh" C-m

#checking once a night for updates
#tmux send-keys -t "pz" "checkModsNeedUpdate"
#tmux capture-pane -t "pz" -p > output.txt
#CheckModsNeedUpdate: Mods updated


#checking for players every 15 minutes
#tmux send-keys -t "pz" "players"
#Players connected (0)
#tmux capture-pane -t "pz" -p > output.txt
#tmux send-keys -t "pz" "exit" C-m


class InstanceManager:
    """Class to manage a specific EC2 instance"""
    def __init__(self):
        session = self.start_session()
        self.instance = self.get_instance(session)

    def get_instance(self, session):
        """Get instance from AWS"""
        ec2 = session.resource('ec2')
        instance = ec2.Instance(EC2_INSTANCE_ID)
        return instance

    def start_session(self):
        """Start a boto3 session with the AWS credentials provided in the environment variables"""
        try:
            session =  boto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )
        except Exception as error:
            # print(error)
            raise error

        return session

    def kill_session(self):
        self.session = None

    def start_instance(self):
        self.instance.start()

    def stop_instance(self):
        self.instance.stop()

    def get_instance_state(self):
        return self.instance.state['Name']

    def get_instance_ip(self):
        return self.instance.public_ip_address
