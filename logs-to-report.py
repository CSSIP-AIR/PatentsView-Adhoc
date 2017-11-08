import re, csv, os
import argparse


def process_logs(log_folder, output_folder, start_date, end_date, ip_string):
    diri = os.listdir(log_folder)
    api_file_name = output_folder + 'API_usage_' + start_date + '-' + end_date + ".csv"
    bulkdownload_file_name = output_folder + 'Bulk_downloads_usage_' + start_date + '-' + end_date + ".csv"
    webtool_file_name = output_folder + 'Webtool_usage_' + start_date + '-' + end_date + ".csv"

    api_file_handle = csv.writer(open(api_file_name, 'wb'))
    bulkdownload_file_handle = csv.writer(open(bulkdownload_file_name, 'wb'))
    webtool_file_handle = csv.writer(open(webtool_file_name, 'wb'))

    for d in diri:
        inp = open(log_folder + d).read().split("\n")

        for i in inp[4:]:
            i = i.split(' ')
            try:
                # for Webtool
                if i[4] == '/web/':
                    webtool_file_handle.writerow([i[0], i[1][:2], i[4], i[5], i[8]])
                # for Bulk downloads stats
                # if re.search('/api/bulk_downloads/',i[4]) or re.search('/data/2015/',i[4]) and not i[-5].startswith("http://www.patentsview.org/web/") and not i[-5].startswith("http://ec2-54-68-66-55."):
                if re.search('/data/', i[4]) and re.search('\.zip', i[4]) and not i[-5].startswith(
                        "http://www.patentsview.org/web/") and not i[-5].startswith("http://ec2-" + ip_string + "."):
                    # outp2.writerow([i[0],i[1][:2],re.search('/(.*?\.zip)',i[4]).group(1),i[5],i[8]])
                    bulkdownload_file_handle.writerow([i[0], i[1][:2], i[4], i[5], i[8]])
                # for API stats
                if re.search('/api/\w+/query', i[4]) and not i[-5].startswith("http://www.patentsview.org/web/") and not \
                        i[
                            -5].startswith("http://ec2-" + ip_string + "."):
                    api_file_handle.writerow([i[0], i[1][:2], i[4], i[5], i[8]])

            except:
                pass


def details(output_folder, name, start_date, end_date):
    input_file = output_folder + name + '_usage_' + start_date + '-' + end_date + '.csv'
    date_detail_file = output_folder + name + '_usage_Date_' + start_date + '-' + end_date + '.csv'
    ip_detail_file = output_folder + name + '_usage_IP_' + start_date + '-' + end_date + '.csv'
    query_detail_file = output_folder + name + '_usage_Query_' + start_date + '-' + end_date + '.csv'
    input_handle = csv.reader(open(input_file, 'rb'))
    date_detail_handle = csv.writer(open(date_detail_file, 'wb'))
    ip_detail_handle = csv.writer(open(ip_detail_file, 'wb'))
    query_detail_handle = csv.writer(open(query_detail_file, 'wb'))

    data = {}
    ips = {}
    query = {}
    for i in input_handle:
        try:
            data[i[0]] += 1
        except:
            data[i[0]] = 1
        try:
            ips[i[-1]] += 1
        except:
            ips[i[-1]] = 1
        try:
            query[i[2] + '_' + i[3]] += 1
        except:
            try:
                query[i[2] + '_' + i[3]] = 1
            except:
                print (i)

    date_detail_handle.writerows(data.items())
    ip_detail_handle.writerows(ips.items())
    query_detail_handle.writerows(query.items())


def uniqipapi(output_folder, name, start_date, end_date):
    input_file = output_folder + name + '_usage_' + start_date + '-' + end_date + '.csv'
    output_file = output_folder + name + '_usage_Date_by_IP_' + start_date + '-' + end_date + '.csv'
    inp = csv.reader(open(input_file, 'rb'))
    outp = csv.writer(open(output_file, 'wb'))

    data = {}
    for i in inp:
        try:
            data[i[0]].append(i[-1])
        except:
            data[i[0]] = [i[-1]]

    for k, v in data.items():
        outp.writerow([k, len(set(v))])


def main():
    parser = argparse.ArgumentParser(description='Report input Parameters')
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-l', type=str, nargs=1, help='The base folder where log files are present',
                                required=True)
    required_named.add_argument('-o', type=str, nargs=1, help='The output folder where reports are created',
                                required=True)
    required_named.add_argument('-s', type=str, nargs=1, help='Report start date (file name only)',
                                required=True)
    required_named.add_argument('-e', type=str, nargs=1, help='Report end date (file name only)',
                                required=True)
    required_named.add_argument('-i', type=str, nargs=1, help='EC2 friendly name',
                                required=True)
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        exit(1)

    log_folder = args.l[0]
    output_folder = args.o[0]
    start_date = args.s[0]  # '09.25'
    end_date = args.e[0]  # '10.31'
    ip_string = args.i[0]  # 34-232-12-12
    process_logs(log_folder, output_folder, start_date, end_date, ip_string)
    details(output_folder, 'Webtool', start_date, end_date)
    details(output_folder, 'API', start_date, end_date)
    details(output_folder, 'Bulk_downloads', start_date, end_date)
    uniqipapi(output_folder, 'Webtool', start_date, end_date)


if __name__ == "__main__":
    main()
