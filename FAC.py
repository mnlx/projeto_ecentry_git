import classexp
import log as lg
import os
import time
while 1:
    log = lg.log()
    log.emailget()
    log_list = []
    lista_analises = []
    email_send = []

    if log.client_list != 'Nothing to be analyzed':
        UC = []
        x=log.client_list[0] # DELETE

        quantity_interruptions = {}
        for i in set(log.client_list):              #transforma itens na lista em unique values
            temp_counter = log.client_list.count(i)
            quantity_interruptions[i] = temp_counter


        for x in log.client_list:           # x será o dominio dos clientes em cada loop
            if x == 'Not a cliente':
                log_list.append(['na'])
                continue
            else:
                print(x)
                analise = classexp.Analise(x)
                try:
                    analise.login()
                except IndexError as e:
                    print(e)
                    continue

                if analise.country == 'Espanha':
                    log_list.append(['na', x, analise.country])
                    analise.driver.close()
                    analise.driver.quit()
                    continue
                else:
                    while True:
                        try:
                            analise.consolidado()
                        except IndexError as e:
                            print(e)
                            continue
                        break
                    while True:
                        try:
                            analise.acc_info()
                        except IndexError as e:
                            print(e)
                            continue
                        break

                    while True:
                        try:
                            analise.specific_report(0)
                        except IndexError as e:
                            print(e)
                            continue
                        break
                    while not analise.del_completa:
                        try:
                            analise.del_seg()
                        except (IndexError) as e:
                            print(e)
                            break
                    num_seg=0
                    while num_seg != 3 :
                        try:
                            analise.criar_seg(num_seg)
                            num_seg += 1
                        except IndexError as e:
                            print(e)
                            pass
                    while 1:

                        try:
                            analise.seg_values()
                            break
                        except:
                            pass

                    analise.driver.close()
                    analise.driver.quit()
            datahora = 'Análise: {0}, {1} hs'.format(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            log_list = log_list + [['a', x, analise.country]]
            save_location = os.path.join(os.path.dirname(__file__),'analises_feitas/{0}/{1}.txt'.format(time.strftime("%d-%m-%Y"),x + ' - ' + analise.campanha[0:15] + ' - ' + str(time.strftime("%d-%m-%Y"))))
            if not os.path.exists(os.path.join(os.path.dirname(__file__),'analises_feitas/{0}'.format(time.strftime("%d-%m-%Y")))):
                os.makedirs(os.path.join(os.path.dirname(__file__),'analises_feitas/{0}'.format(time.strftime("%d-%m-%Y"))))
            with open(save_location,'w') as f1:
                f1.write(str(datahora) + os.linesep)
                f1.write('Campanha:' + analise.campanha + os.linesep)
                f1.write('Listas de inclusão: {0}'.format(analise.lista[0]) + os.linesep)
                f1.write('Listas de exclusão: {0}'.format(analise.lista[1]) + os.linesep)
                f1.write('Segmentação: {0}'.format(analise.lista[2]) + os.linesep)
                f1.write('Denuncias: {0}'.format(analise.denuncias) + os.linesep)
                f1.write('Cancelamentos: {0}'.format(analise.cance) + os.linesep)
                f1.write('Erros permanentes: {6} ({7}%) - {2} ({3}%) usuários desconhecidos, {0} ({1}%) endereço(s) inativo(s), {4} ({5}%) erros de domínio desconhecido'.format(analise.erros[0], analise.erros[1], analise.erros[2], analise.erros[3], analise.erros[4], analise.erros[5], analise.erros[6], analise.erros[7]) + os.linesep)

                f1.write(os.linesep)
                f1.write('SPF: {0} OK e {1} Falha(s)'.format(analise.spf.count('Autenticado'), analise.spf.count('Falhou')) + os.linesep)
                f1.write('DKIM: {0} OK e {1} Falha(s)'.format(analise.dkim.count('Autenticado'), analise.dkim.count('Falhou')) + os.linesep)
                f1.write('Domínio próprio: {0} de 2 OK'.format(analise.valido) + os.linesep)

                f1.write(os.linesep)
                f1.write("Qualidade de Base: " + analise.quali + os.linesep)
                f1.write("Contatos base: " + analise.cadast + os.linesep)
                f1.write("Campanhas interrompidas no mês: " + os.linesep)
                f1.write("Interação 6 meses: {0}".format(analise.segmen[0]) + os.linesep)
                f1.write('Interação 12 meses: {0}'.format(analise.segmen[1]) + os.linesep)
                f1.write('Nunca Interagiram: {0}'.format(analise.segmen[2]) + os.linesep)
                f1.write('Media visualização 3 meses:{0: .2f}%'.format(analise.visua_mean) + os.linesep)
                f1.write('Media clicks 3 meses:{0: .2f}%'.format(analise.clicks_mean) + os.linesep)
            f1.close()
            lista_analises.append(analise)
            email_send.append([save_location, x, analise.campanha[0:15]])

        log.emailsend(email_send)       #sends all analyzed campaigns to analiseecentry@gmail.com
        log.loger(log_list)             #logs all analyzed campaigns








# datahora = 'Análise: {0}, {1} hs'.format(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
#

#
#
#
