import boto3
from prettytable import PrettyTable

def lambda_handler(event, context):
    
    ec2_name = event.get('instance_id')
    ec2 = boto3.client('ec2')

    response_ec2 = ec2.describe_instances(
        Filters=[{
            'Name': 'instance-id',
            'Values': [f'*{ec2_name}*']
        }],
    )

    response_volumes = ec2.describe_volumes()

    l_instance = []
    count = 0

    def get_Volumes(ec2id):
        total_sum = 0
        for i in response_volumes['Volumes']:
            if i['Attachments']:
                if i['Attachments'][0]['InstanceId'] == ec2id:
                    total_sum += i['Size']
        return total_sum

    for i in response_ec2['Reservations']:
        for j in i['Instances']:
            l_instance.append([j['InstanceId'], j['InstanceType'], j['State']['Name'], j['PrivateIpAddress']])
            if 'PublicIpAddress' in j:
                l_instance[count].append(j['PublicIpAddress'])
            else:
                l_instance[count].append('Not Available')
            l_instance[count].append(get_Volumes(j['InstanceId']))
            count += 1

    l_instance = sorted(l_instance, key=lambda x: int(x[5]), reverse=True)

    sum_size_ebs = 0
    for i in l_instance:
        sum_size_ebs += i[5]

    tab = PrettyTable(['instance-id', 'instance-type', 'status', 'private-ip', 'public-ip', 'total-size-ebs-volumes'])

    tab.add_rows(l_instance)
    tab.add_row(["-" * 10, "-" * 10, "-" * 10, "-" * 10, "-" * 10, "-" * 10])
    tab.add_row(['', '', '', '', 'sum ebs vol', sum_size_ebs])

    # Convert PrettyTable to a JSON-friendly format
    table_result = []
    for row in tab.get_string().splitlines():
        table_result.append(row.split('|')[1:-1])

    print(tab)
    return {
        'statusCode': 200,
        'body': {
            'result': table_result
        }
    }
