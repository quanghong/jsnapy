from lxml import etree
import os
from jnpr.jsnap.sqlite_store import JsnapSqlite
import sys


class Parse:

    # generate snap files for devices based on given commands and rpc
    def generate_reply(self, test_file, dev, snap_files, db, username):
        """
        generate rpc reply based on given commands/ rpc

        :param test_file: test file containing test cases
        :param dev: device handler
        :param snap_files: files to store snapshots
        :param db: name of database
        :param username: device's username
        :return:
        """
        print "\nTaking snapshots of............" 
        self.command_list = []
        self.rpc_list = []
        self.test_included = []
        path = os.getcwd()
        if 'tests_include' in test_file:
            for t in test_file.get('tests_include'):
                self.test_included.append(t)
                if t in test_file:
                    if test_file.get(t) is not None and (
                            'command' in test_file[t][0]):
                        command = test_file[t][0].get(
                            'command',
                            "unknown command")
                        self.command_list.append(command)
                        name = '_'.join(command.split())
                        try:
                            print "\nTaking snapshot for %s"%command
                            rpc_reply_command = dev.rpc.cli(
                                command,
                                format='xml')
                        except Exception:
                            print "ERROR occurred ----!!!", sys.exc_info()[0]
                            print "\n**********Complete error message***********\n", sys.exc_info()
                        else:
                            filename = snap_files + '_' + name + '.' + 'xml'
                            output_file = os.path.join(
                                path,
                                'snapshots',
                                filename)
                            with open(output_file, 'w') as f:
                                f.write(etree.tostring(rpc_reply_command))

                            # SQLiteChanges
                            if db['store_in_sqlite'] is True:
                                a = snap_files.split('_')
                                host = a[0]
                                a.pop(0)
                                a = '_'.join(a)
                                sqlite_jsnap = JsnapSqlite(host, db['db_name'])
                                db_dict = dict()
                                db_dict['username'] = username
                                db_dict['cli_command'] = name
                                db_dict['snap_name'] = a
                                db_dict['filename'] = filename
                                db_dict['xml'] = etree.tostring(
                                    rpc_reply_command)
                                sqlite_jsnap.insert_data(db_dict)
                            ###

                    elif test_file.get(t) is not None and 'rpc' in test_file[t][0]:
                        rpc = test_file[t][0].get('rpc', "unknown rpc")
                        self.rpc_list.append(rpc)
                        if len(test_file[t]) >= 2 and 'args' in test_file[
                                t][1]:
                            kwargs = {
                                k.replace(
                                    '-',
                                    '_'): v for k,
                                v in test_file[t][1]['args'].items()}
                            if 'filter_xml' in kwargs:
                                from lxml.builder import E
                                filter_data = None
                                for tag in kwargs[
                                        'filter_xml'].split('/')[::-1]:
                                    filter_data = E(tag) if filter_data is None else E(
                                        tag,
                                        filter_data)
                                    kwargs['filter_xml'] = filter_data
                            try:
                                print "\nTaking snapshot of %s" %rpc
                                rpc_reply = getattr(
                                    dev.rpc,
                                    rpc.replace(
                                        '-',
                                        '_'))(
                                    **kwargs)
                            except Exception:
                                print "ERROR occurred ----!!!", sys.exc_info()[0]
                                print "\n**********Complete error message***********\n", sys.exc_info()
                        else:
                            try:
                                print "\nTaking snapshot of %s" %rpc
                                rpc_reply = getattr(
                                    dev.rpc,
                                    rpc.replace(
                                        '-',
                                        '_'))()
                            except Exception:
                                print "ERROR occurred ----!!!", sys.exc_info()[0]
                                print "\n**********Complete error message***********\n", sys.exc_info()

                        if 'rpc_reply' in locals():
                            filename = snap_files + '_' + rpc + '.' + 'xml'
                            output_file = os.path.join(
                                path,
                                'snapshots',
                                filename)
                            with open(output_file, 'w') as f:
                                f.write(etree.tostring(rpc_reply))

                            # SQLiteChanges
                            if db['store_in_sqlite'] is True:
                                a = snap_files.split('_')
                                host = a[0]
                                a.pop(0)
                                a = '_'.join(a)
                                sqlite_jsnap = JsnapSqlite(host, db['db_name'])
                                db_dict2 = dict()
                                db_dict2['username'] = username
                                db_dict2['cli_command'] = rpc
                                db_dict2['snap_name'] = a
                                db_dict2['filename'] = filename
                                db_dict2['xml'] = etree.tostring(rpc_reply)
                                sqlite_jsnap.insert_data(db_dict2)
                        ###
                    else:
                        print "ERROR!!! Test case: '%s' not defined properly" % t
                else:
                    print "ERROR!!! Test case: '%s' not defined !!!!" % t
        else:
            print "\nERROR!! None of the test cases included"
