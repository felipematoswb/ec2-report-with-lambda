import boto3

from prettytable import PrettyTable


#instance a ec2 from boto3
ec2 = boto3.client('ec2')

#request ID from user
ec2_name = input('Given an Instance ID (default: *): ')

#search ec2 instance, no matter if user pass a ID or no.
response_ec2 = ec2.describe_instances(
    Filters=[{
        'Name': 'instance-id',
        'Values': [f'*{ec2_name}*']
    }], 
)

#search volumes, take all in one request.
response_volumes = ec2.describe_volumes()

#create a list to append rows of table
l_instance = []

# a function to search volumes by InstanceId
def get_Volumes(ec2id):
    total_sum = 0
    for i in response_volumes['Volumes']:
        if i['Attachments']:
            if i['Attachments'][0]['InstanceId'] == ec2id:
                total_sum += i['Size']
    return(total_sum)

# a count to append values in correct index 
count = 0

# a for to iteract inside ec2 response
for i in response_ec2['Reservations']:
    
    for j in i['Instances']:
        
        l_instance.append([ j['InstanceId'], j['InstanceType'], j['State']['Name'], j['PrivateIpAddress'] ])
        
        if 'PublicIpAddress' in j:
            l_instance[count].append(j['PublicIpAddress'])
        else:
            l_instance[count].append('Not Avaliable')
        l_instance[count].append(get_Volumes(j['InstanceId']))
        count+=1

# organize a list by volume size
l_instance = sorted(l_instance, key=lambda x: int(x[5]), reverse=True)

# sum volumes size
sum_size_ebs = 0
for i in l_instance:
    sum_size_ebs += i[5]

# add a column table title
tab = PrettyTable(['instance-id', 'instance-type', 'status', 'private-ip', 'public-ip', 'total-size-ebs-volumes'])

# add rows to table
tab.add_rows(l_instance)

# add a line to separate result between total ebs size
tab.add_row(["-" * 10, "-" * 10, "-" * 10, "-" * 10, "-" * 10, "-" * 10])

# add a row total and total volume size
tab.add_row(['','','','','sum ebs vol',sum_size_ebs])

# print search result
print(tab)