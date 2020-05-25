Search.setIndex({docnames:["client/app","client/controllers","client/db","client/decorators","client/descriptors","client/handlers","client/local_controllers","client/log","client/metaclasses","client/modules","client/protocol","client/resolvers","client/settings","client/ui","client/utils","index","server/app","server/controllers","server/db","server/decorators","server/descriptors","server/handler","server/log","server/metaclasses","server/modules","server/protocol","server/resolver","server/security","server/settings","server/ui","server/utils"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.index":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,sphinx:56},filenames:["client\\app.rst","client\\controllers.rst","client\\db.rst","client\\decorators.rst","client\\descriptors.rst","client\\handlers.rst","client\\local_controllers.rst","client\\log.rst","client\\metaclasses.rst","client\\modules.rst","client\\protocol.rst","client\\resolvers.rst","client\\settings.rst","client\\ui.rst","client\\utils.rst","index.rst","server\\app.rst","server\\controllers.rst","server\\db.rst","server\\decorators.rst","server\\descriptors.rst","server\\handler.rst","server\\log.rst","server\\metaclasses.rst","server\\modules.rst","server\\protocol.rst","server\\resolver.rst","server\\security.rst","server\\settings.rst","server\\ui.rst","server\\utils.rst"],objects:{"":{app:[16,0,0,"-"],controllers:[17,0,0,"-"],db:[18,0,0,"-"],decorators:[19,0,0,"-"],descriptors:[20,0,0,"-"],handler:[21,0,0,"-"],log:[22,0,0,"-"],metaclasses:[23,0,0,"-"],protocol:[25,0,0,"-"],resolver:[26,0,0,"-"],security:[27,0,0,"-"],settings:[28,0,0,"-"],ui:[29,0,0,"-"],utils:[30,0,0,"-"]},"app.Server":{bufsize:[16,2,1,""],get_request:[16,3,1,""],host:[16,2,1,""],init_session:[16,3,1,""],port:[16,2,1,""],run:[16,3,1,""]},"db.database":{migrate_db:[18,4,1,""],session_scope:[18,4,1,""]},"db.models":{ActiveClient:[18,1,1,""],Client:[18,1,1,""],ClientContact:[18,1,1,""],ClientSession:[18,1,1,""],Message:[18,1,1,""],on_active_clients_changed:[18,4,1,""]},"db.models.ActiveClient":{addr:[18,2,1,""],client:[18,2,1,""],client_id:[18,2,1,""],client_name:[18,2,1,""],created:[18,2,1,""],id:[18,2,1,""],port:[18,2,1,""]},"db.models.Client":{entry_in_active:[18,2,1,""],friends:[18,2,1,""],gotten_messages:[18,2,1,""],id:[18,2,1,""],name:[18,2,1,""],owners:[18,2,1,""],password:[18,2,1,""],sent_messages:[18,2,1,""],sessions:[18,2,1,""]},"db.models.ClientContact":{confirmed:[18,2,1,""],friend_contact:[18,2,1,""],friend_id:[18,2,1,""],id:[18,2,1,""],owner_contact:[18,2,1,""],owner_id:[18,2,1,""]},"db.models.ClientSession":{client:[18,2,1,""],client_id:[18,2,1,""],closed:[18,2,1,""],created:[18,2,1,""],id:[18,2,1,""],local_addr:[18,2,1,""],local_port:[18,2,1,""],remote_addr:[18,2,1,""],remote_port:[18,2,1,""],token:[18,2,1,""]},"db.models.Message":{created:[18,2,1,""],edited:[18,2,1,""],from_client:[18,2,1,""],from_client_id:[18,2,1,""],id:[18,2,1,""],text:[18,2,1,""],to_client:[18,2,1,""],to_client_id:[18,2,1,""]},"db.utils":{add_client_to_active_list:[18,4,1,""],authenticate:[18,4,1,""],clear_active_clients_list:[18,4,1,""],get_client_stats:[18,4,1,""],get_connections:[18,4,1,""],get_validation_errors:[18,4,1,""],login:[18,4,1,""],remove_from_active_clients:[18,4,1,""]},"security.middlewares":{encryption_middleware:[27,4,1,""]},"security.utils":{get_chunk:[27,4,1,""]},"ui.app":{GUIApplication:[29,1,1,""]},"ui.app.GUIApplication":{connect_main_window_buttons:[29,3,1,""],get_validation_errors:[29,3,1,""],host:[29,2,1,""],make_signals_connection:[29,3,1,""],port:[29,2,1,""],render:[29,3,1,""],render_connections_table:[29,3,1,""],save_config_to_file:[29,3,1,""],show_client_stats_window:[29,3,1,""],show_config_window:[29,3,1,""],show_main_window:[29,3,1,""]},"ui.client_stats_window":{ClientStatsWindow:[29,1,1,""]},"ui.client_stats_window.ClientStatsWindow":{close_and_destroy:[29,3,1,""]},"ui.config_window":{ConfigWindow:[29,1,1,""]},"ui.config_window.ConfigWindow":{clear_close_and_destroy:[29,3,1,""],open_file_dialog:[29,3,1,""]},"ui.main_window":{MainWindow:[29,1,1,""]},"ui.signals":{SenderObject:[29,1,1,""]},"ui.signals.SenderObject":{active_client_signal:[29,2,1,""]},"ui.utils":{create_new_row:[29,4,1,""],get_client_stats_table:[29,4,1,""],get_connections_table:[29,4,1,""],get_row_list:[29,4,1,""]},app:{Server:[16,1,1,""]},controllers:{add_contact_controller:[17,4,1,""],del_contact_controller:[17,4,1,""],del_message_controller:[17,4,1,""],get_contacts_controller:[17,4,1,""],get_messages_controller:[17,4,1,""],login_controller:[17,4,1,""],logout_controller:[17,4,1,""],message_controller:[17,4,1,""],presence_controller:[17,4,1,""],register_controller:[17,4,1,""],upd_message_controller:[17,4,1,""]},db:{database:[18,0,0,"-"],models:[18,0,0,"-"],settings:[18,0,0,"-"],utils:[18,0,0,"-"]},decorators:{compression_middleware:[19,4,1,""],json_middleware:[19,4,1,""],log:[19,4,1,""],login_required:[19,4,1,""]},descriptors:{BufsizeValidator:[20,1,1,""],HostValidator:[20,1,1,""],PortValidator:[20,1,1,""]},handler:{handle_request:[21,4,1,""]},log:{log_config:[22,0,0,"-"]},metaclasses:{ServerVerifier:[23,1,1,""]},protocol:{get_socket_info_from_request:[25,4,1,""],is_request_valid:[25,4,1,""],make_response:[25,4,1,""]},resolver:{get_controller:[26,4,1,""]},security:{middlewares:[27,0,0,"-"],settings:[27,0,0,"-"],utils:[27,0,0,"-"]},ui:{app:[29,0,0,"-"],client_stats_window:[29,0,0,"-"],config_window:[29,0,0,"-"],main_window:[29,0,0,"-"],signals:[29,0,0,"-"],utils:[29,0,0,"-"]},utils:{get_config:[30,4,1,""],get_config_from_yaml:[30,4,1,""],get_receiver_addr_and_port:[30,4,1,""],get_socket_info:[30,4,1,""],parse_args:[30,4,1,""],write_config_to_yaml:[30,4,1,""]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:function"},terms:{"byte":[3,19],"class":[0,3,4,8,13,16,18,19,20,23,26,29],"function":[3,14,19,26,27,30],"int":[10,25],"return":[3,10,14,19,21,25,26,30],"true":[10,18,25],The:26,accept:[0,16],action:26,action_nam:26,activ:18,active_client_sign:[13,29],activecli:18,add:[0,14,16,30],add_client_to_active_list:[2,18],add_contact_control:[1,17],add_contact_window:9,added:[14,30],addr:[2,14,18,30],addr_typ:[10,25],address:[10,25],all:[10,25],also:[3,19],ani:21,api:18,app:[1,2,4,8,9,10,12,14,15,17,18,20,21,23,24,25,26,28,30],arg:[3,14,19,30],argpars:[14,30],argument:[14,30],associ:26,attr:[2,18],attribut:[2,18],authent:[2,18],backlog:[0,16],base:[0,2,3,4,8,10,13,16,18,19,20,23,25,29],basic:[7,22],bind:[0,16],block:[0,16],bodi:[10,21,25],bool:[10,25],buffers:[0,4,16,20],bufsiz:[0,16],bufsizevalid:[4,20],call:[3,19],caller:[3,19],chang:18,check:[3,10,19,25],chunk:27,clear_active_clients_list:[2,18],clear_close_and_destroi:29,client:[0,2,10,15,16,18,21,25,26],client_id:18,client_nam:18,client_stats_window:24,clientcontact:18,clients_db:9,clientsess:18,clientstatswindow:29,close:18,close_and_destroi:29,clsdict:[8,23],clsname:[8,23],code:[10,25],command:[14,30],compress:[3,19],compression_middlewar:[3,19],config:[14,30],config_window:24,configur:[7,22],configwindow:29,confirm:18,connect:18,connect_main_window_button:[13,29],contact:18,content:[9,15,24],context:18,control:[9,15,24,26],creat:[14,18,30],create_new_row:[13,29],data:[10,14,25,30],databas:[2,24],declar:18,decompress:[3,19],decor:[9,15,24],decrypt:27,del_contact_control:[1,17],del_contact_window:9,del_message_control:[1,17],descriptor:[9,15,24],dict:[3,10,19,21,25],edit:18,encrypt:27,encryption_middlewar:27,entry_in_act:18,error:[2,18],exist:[3,19],expir:18,ext:18,fals:[10,25],filenam:[14,30],friend:18,friend_contact:18,friend_id:18,from:[0,10,16,21,25,26,27],from_client:18,from_client_id:18,func:[3,19,27],geekbrain:[14,30],get:[0,2,10,16,18,21,25,26,27],get_chunk:27,get_client_stat:[2,18],get_client_stats_t:[13,29],get_config:[14,30],get_config_from_yaml:[14,30],get_connect:[2,18],get_connections_t:[13,29],get_contacts_control:[1,17],get_control:26,get_messages_control:[1,17],get_receiver_addr_and_port:[14,30],get_request:[0,16],get_row_list:[13,29],get_socket_info:[14,30],get_socket_info_from_request:[10,25],get_validation_error:[2,13,18,29],github:[14,30],gotten_messag:18,guiapplic:[13,29],handl:[0,3,16,19,21],handle_request:21,handler:[9,15,24],host:[0,4,13,16,20,29],hostvalid:[4,20],index:15,init_sess:[0,16],initi:[0,16],is_request_valid:[10,25],json:[3,19],json_middlewar:[3,19],kei:[10,25,26],kwarg:[3,18,19],l_addr:[10,25],line:[14,30],list:[0,16],listen:[0,16],load:[3,19],local:[10,25],local_addr:18,local_control:[9,15],local_port:18,local_storag:9,log:[2,3,9,15,18,19,24],log_config:[9,24],login:[2,18],login_control:[1,17],login_requir:[3,19],login_window:9,logout_control:[1,17],made:18,main:[0,16],main_window:[9,24],mainwindow:[13,29],make:[2,10,18,25,27],make_respons:[10,25],make_signals_connect:[13,29],manag:18,mapper:18,messag:[10,18,25],message_control:[1,17],messeng:[0,1,2,3,4,8,10,12,14,16,17,18,19,20,21,23,25,26,28,30],metaclass:[9,15,24],middlewar:24,migrate_db:18,model:24,modul:[9,15,24],name:[3,18,19,26],namedtupl:[10,25],namespac:[14,30],non:[0,16],none:[10,25],object:[0,4,13,16,20,29],on_active_clients_chang:18,open_file_dialog:29,otherwis:[10,25],owner:18,owner_contact:18,owner_id:18,packag:[9,15,24],page:15,pair:[10,25],param:[0,3,10,14,16,19,21,25,26,30],parse_arg:[14,30],parser:[14,30],pass:[3,10,19,25,26],password:[2,18],port:[0,2,4,10,13,14,16,18,20,25,29,30],portvalid:[4,20],presence_control:[1,17],propag:18,protocol:[9,15,24],protocol_object:[14,30],pyqt5:[13,29],qdialog:29,qmainwindow:[13,29],qobject:[13,29],qtcore:[13,29],qtwidget:[13,29],r_addr:[10,25],read:[0,16],receiv:27,register_control:[1,17],remot:[10,25],remote_addr:18,remote_port:18,remove_from_active_cli:[2,18],render:[13,29],render_connections_t:[13,29],request:[0,1,2,3,10,16,17,18,19,21,25,27],residu:27,resolv:[9,15,24],respons:[0,10,16,21,25,27],result:[3,19],row_nam:[13,29],run:[0,16],save_config_to_fil:[13,29],schema:18,search:15,secur:[15,24],senderobject:[13,29],sent_messag:18,server:[0,1,2,3,4,7,8,10,12,13,14,15,16,17,18,19,20,21,22,23,25,26,28,29,30],serververifi:[8,23],session:[0,2,16,18],session_scop:18,set:[9,15,24],show_client_stats_window:[13,29],show_config_window:[13,29],show_main_window:[13,29],side:[0,1,2,3,4,8,10,12,14,16,17,18,19,20,21,23,25,26,28,30],signal:[9,24],signup_window:9,size:27,socket:[0,16],some:[2,18],sqlalchemi:18,statu:[10,25],str:[10,25,26],submodul:[9,24],system:[7,22],target:18,text:[18,27],than:27,them:[0,16],thi:26,thread:[0,16],to_client:18,to_client_id:18,token:[2,3,18,19],too:[3,19],transmit:[10,25],tupl:[14,30],type:[8,10,23,25],upd_message_control:[1,17],user:[3,14,19,30],util:[9,15,24],valid:[0,2,3,4,10,13,16,18,19,20,25,29],valu:26,verifi:[8,23],where:[3,19],write:[0,16],write_config_to_yaml:[14,30],yandexdisk:[14,30],yml:[14,30]},titles:["app module","controllers module","db package","decorators module","descriptors module","handlers module","local_controllers module","log package","metaclasses module","client","protocol module","resolvers module","settings module","ui package","utils module","Welcome to Messenger\u2019s documentation!","app module","controllers module","db package","decorators module","descriptors module","handler module","log package","metaclasses module","server","protocol module","resolver module","security package","settings module","ui package","utils module"],titleterms:{add_contact_window:13,app:[0,13,16,29],client:9,client_stats_window:29,clients_db:2,config_window:29,content:[2,7,13,18,22,27,29],control:[1,17],databas:18,decor:[3,19],del_contact_window:13,descriptor:[4,20],document:15,handler:[5,21],indic:15,local_control:6,local_storag:2,log:[7,22],log_config:[7,22],login_window:13,main_window:[13,29],messeng:15,metaclass:[8,23],middlewar:27,model:18,modul:[0,1,2,3,4,5,6,7,8,10,11,12,13,14,16,17,18,19,20,21,22,23,25,26,27,28,29,30],packag:[2,7,13,18,22,27,29],protocol:[10,25],resolv:[11,26],secur:27,server:24,set:[2,12,18,27,28],signal:[13,29],signup_window:13,submodul:[2,7,13,18,22,27,29],tabl:15,util:[2,13,14,18,27,29,30],welcom:15}})