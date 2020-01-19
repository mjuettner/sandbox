# Playing with Puppet

## Setup
- Create a new EC2 Key Pair named 'puppet'
- Deploy the vpc.yaml CloudFormation template to create a basic network infrastructure, you will need an Internet Gateway, but not any NAT Gateways
- Deploy the puppet-sg.yaml CloudFormation template to create the Security Group to use with the EC2 instances
- Deploy the puppet-master.yaml CloudFormation template to create the Master Puppet Server
- Deploy the puppet-slaves.yaml CloudFormation template to create a few Puppet Slaves
  - Update the UserData section to modify the echo command with the internal DNS name of your Master server
  - As these slaves come online and set up the Puppet Agent, you will see them register with the Master and you can sign and accept their certificate requests
```bash
[root@ip-10-0-1-132 ~]# puppetserver ca list
Requested Certificates:
    ip-10-0-13-250.ec2.internal   (SHA256)  53:EF:2A:85:BD:D4:7A:67:C7:F3:F8:0B:F6:C5:13:11:BD:39:B0:CC:96:FC:14:DA:8C:88:9D:E4:48:7A:D0:6F
    ip-10-0-21-63.ec2.internal    (SHA256)  5D:DC:A7:CF:57:15:4B:6F:52:B9:C4:2E:88:54:BA:2C:89:CA:70:42:58:53:18:97:54:AE:86:0F:99:00:18:87
    ip-10-0-42-168.ec2.internal   (SHA256)  3D:F7:F4:67:55:D0:EC:54:21:37:2E:58:4C:50:EF:B6:85:B7:DA:9D:50:8C:E3:2C:ED:79:0B:EE:3F:27:09:64

[root@ip-10-0-1-132 ~]# puppetserver ca sign --all
Successfully signed certificate request for ip-10-0-13-250.ec2.internal
Successfully signed certificate request for ip-10-0-21-63.ec2.internal
Successfully signed certificate request for ip-10-0-42-168.ec2.internal
```

## Usage
- Start writing and pushing Manifests and Modules now

## Cleanup
- Delete all the CloudFormation stacks
