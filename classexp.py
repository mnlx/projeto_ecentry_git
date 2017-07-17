from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
import datetime

class pQuery():

    #Classe de seletores da análise, a ideia é ser parecido com jQuery

    def __init__(self):
        print('pQuery class created')

    def xpath(self, analisedriver, htmltag, htmlidentifier ='empty', htmlidentname='empty',selector = ''):
        #selector serve para ter certeza que todos os elementos foram carregados na página.

        self.overrepeater = False
        PING = 0.1
        while True:
            try:
                # Parte necessária para caso a pessoa deseja selecionar apenas a classe sem saber o tag
                if  htmltag == 'empty':

                    overrepeater = 0 #serve para limitar o número de busca de elementos em uma página
                    wait_load_list = []
                    l = 0
                    while True:
                        if htmlidentname[-1] == ' ':
                            htmlidentname = htmlidentname[0:-1]
                        elem = analisedriver.find_elements_by_css_selector('.{0}'.format(htmlidentname.replace(' ','.')))
                        print(len(elem))
                        if selector == 'list':
                            wait_load_list.append(len(elem))
                            if l > 2:
                                if wait_load_list[-1] == wait_load_list[-3]:
                                    break
                                else:
                                    pass
                            else:
                                l += 1

                        elif len(elem) >= selector+1:
                            break
                        elif overrepeater >100:
                            break
                        time.sleep(PING)
                        overrepeater += 1
                    break

                elif htmlidentifier != 'empty':

                    overrepeater = 0 #serve para limitar o número de busca de elementos em uma página
                    wait_load_list = []
                    l = 0

                    while True:

                        elem = analisedriver.find_elements_by_xpath("//{0}[@{1}='{2}']".format(htmltag, htmlidentifier,
                                                                                                     htmlidentname))
                        if selector == 'list':
                            wait_load_list.append(len(elem))

                            if l > 2:
                                if wait_load_list[-1] == wait_load_list[-3]:
                                    break
                                else:
                                    pass
                            else:
                                l += 1
                        elif len(elem) >= selector+1:
                            break
                        elif overrepeater >100:
                            break
                        # elit len(elem) == 0
                        time.sleep(PING)
                        print(overrepeater)
                        overrepeater += 1
                    break
                elif htmlidentifier== 'empty':
                    overrepeater = 0
                    wait_load_list = []
                    l = 0
                    while True:
                        elem = analisedriver.find_elements_by_xpath("//{0}".format(htmltag))

                        if selector == 'list':
                            wait_load_list.append(len(elem))
                            if l > 2:
                                if wait_load_list[-1] == wait_load_list[-3]:
                                    break
                                else:
                                    pass
                            else:
                                l += 1
                        elif len(elem) >= selector+1:
                            break
                        elif overrepeater >100:
                            break
                        time.sleep(PING)
                        overrepeater += 1
                    break

            except selenium.common.exceptions.NoSuchElementException as e:
                print(e + ' Procurando novamente')
        if overrepeater >= 100:
            print('+++++++++++++++++Over repeater has been trigered!')
            self.overrepeater = True
        else:
            self.listelem = elem

    def selector(self, elemnum):
        if elemnum == 'list':
            return self.listelem
        else:
            return self.listelem[elemnum]

    def click(self, elenum):
        self.listelem[elenum].click()

    def attribute(self,elenum ,atr):
        return self.listelem[elenum].get_attribute(atr)



class Analise():

    #Classe base da análise

    def __init__(self,dominio):
        print('started')
        self.driver = webdriver.Firefox()
        self.URL = "http://{0}.emailmanager.com".format(dominio)
        self.del_completa = False

        self.query = pQuery()

        global xp
        xp = self.query.xpath

    def click(self,id_class):
        try:
            e = self.driver.find_element_by_class_name(id_class)
        except:
            e.click()
        e.click()

    def xpath(self,locator ,isclass , classname ,n=0 ):
        # Função proucura elementos por meio de XPATH
        # Será necessário acrescentar mais locators (id,img,...)

        if n == 0:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//{0}[@{1}='{2}']".format(locator,isclass,classname))))
            return self.driver.find_element(By.XPATH, "//{0}[@{1}='{2}']".format(locator, isclass, classname))
        elif n>0:
            #Não há como esperar para uma lista carregar, portanto temos que procurar por um elemento apenas
            init = 1
            final = -1
            while init != final:
                init = len(self.driver.find_elements(By.XPATH, "//{0}[@{1}='{2}']".format(locator, isclass, classname)))
                time.sleep(1)
                final = len(self.driver.find_elements(By.XPATH, "//{0}[@{1}='{2}']".format(locator, isclass, classname)))
            return self.driver.find_elements(By.XPATH, "//{0}[@{1}='{2}']".format(locator, isclass, classname))

    def login(self):
        URL= self.URL
        self.driver.get(URL)
        self.country = 'Brasil'
        if '¿Olvidó su contraseña?' in self.driver.page_source:
            print('yes')
            self.country = 'Espanha'
        elif 'Did you forget your password?' in self.driver.page_source:
            self.country = 'USA'
        elem = self.driver.find_element_by_name("login")
        elem.clear()
        elem.send_keys("andre.duarte/admin")
        elem2 = self.driver.find_element_by_id('pass')
        elem2.send_keys("75KZd55n")
        self.click('bt-gr-orange')
        print('go')
        # time.sleep(8)


        #################################################################abaixo des temp
        # try:
        #     xp(self.driver, 'div', 'class',
        #        'x-btn app-btn orange add x-box-item x-toolbar-item x-btn-default-toolbar-medium x-noicon x-btn-noicon x-btn-default-toolbar-medium-noicon',
        #        0)
        #     # try:
        #      ##criar tempo para executar script filler
        #     self.driver.execute_script( "document.getElementsByClassName('x-btn app-btn orange add x-box-item x-toolbar-item x-btn-default-toolbar-medium x-noicon x-btn-noicon x-btn-default-toolbar-medium-noicon').item(0).click();")
        # except selenium.common.exceptions.WebDriverException as e:
        #     print(e)
        #################################################################acima des temp




        # elem = self.driver.find_elements_by_xpath(
        #     "//div[@class='x-btn app-btn orange add x-box-item x-toolbar-item x-btn-default-toolbar-medium x-noicon x-btn-noicon x-btn-default-toolbar-medium-noicon']")
        # elem[0].click()
        # except:
        #     print('all good')

        # time.sleep(1)
        #################################################################abaixo des temp
        # try:
        #     xp(self.driver, 'img', 'class',
        #        'x-tool-close',
        #        0)
        #     self.query.click(0)
        #     # elem = self.driver.find_elements_by_xpath("//img[@class='x-tool-close']")
        #     # elem[0].click()
        # except:
        #     print('all good')
        #################################################################acima des temp

    def consolidado(self):

        def table_get(driver):
            elem = driver.find_elements_by_tag_name('td')
            return [str(x.text) for x in elem]

        def table_value(table_list, index):
            ind = table_list.index(index)
            visualstr = table_list[ind + 1]
            return float(visualstr.split('(')[1].split('%')[0].replace(',', '.'))

        URL = self.URL
        self.driver.get(URL + "/#Report/Consolidated")
        self.visua = []
        self.clicks = []
        # time.sleep(7)
        for x in range(3):
            try:
                xp(self.driver, 'table', 'class', 'x-form-trigger-wrap',0)
                self.query.click(0)
                xp(self.driver, 'li', 'empty', 'empty' , x)
                self.query.click(x)

                if self.query.overrepeater:
                    self.query.overrepeater = False
                    break

                try:
                    elem = table_get(self.driver)
                    self.visua.append(table_value(elem, "total de visualizações"))
                    self.clicks.append(table_value(elem, "total de cliques"))
                except:
                    self.visua.append( "NaN") # caso não haja dados BR
                    self.clicks.append( "NaN") # caso não haja dados BR
                    pass
                try:
                    elem = table_get(self.driver)
                    self.visua.append(table_value(elem, "total views")) # para clientes americanos
                    self.clicks.append(table_value(elem, "total clicks")) # para clientes americanos
                except:
                    self.visua.append( "NaN") # caso não haja dados  US
                    self.clicks.append( "NaN") # caso não haja dados  US
                    pass

            except IndexError:
                print('No visualizations or click data for month {0}'.format(x))
        # print(self.visua)
        mean = []
        for x in self.visua:
            if type(x)==float:
                mean.append(x)
        self.visua_mean = sum(mean)/len(mean)

        mean = []
        for x in self.clicks:
            if type(x)==float:
                mean.append(x)
        self.clicks_mean = sum(mean)/len(mean)

    def acc_info(self):

        URL = self.URL
        self.driver.get(URL + "/#ControlPanel/Domain")


        # Obtendo informações do dominio
        time.sleep(2)

        # elem = self.driver.find_elements_by_tag_name('img')
        self.valido = 0
        repeat = 0
        while True:
            xp(self.driver, 'img', 'empty', 'empty', 1)
            if 'ic_valido.png' in self.query.attribute(0,'src') and 'ic_valido.png' in self.query.attribute(1,'src') :
                self.valido = 2
                break
            elif repeat>30:
                self.valido = 0
                break
            else:
                repeat += 1
                time.sleep(0.1)

        # SPF e DKIM
        # Needs improvement
        self.driver.get(URL + "/#ControlPanel/AccountSender")
        time.sleep(2)
        xp(self.driver, 'td', 'empty', 'empty', 'list')
        elem_list = self.query.selector('list')

        elem_sing = [x.text for x in elem_list]
        while '' in elem_sing:
            elem_sing.remove('')
        while 'Verificada' in elem_sing:
            elem_sing.remove('Verificada')
        while 'Verificar\nEditar\nApagar' in elem_sing:
            elem_sing.remove('Verificar\nEditar\nApagar')
        while 'Editar\nApagar' in elem_sing:
            elem_sing.remove('Editar\nApagar')
        while 'Não verificada' in elem_sing:
            elem_sing.remove('Não verificada')
        while 'Verified' in elem_sing:
            elem_sing.remove('Verified')
        while 'Verified\nEdit\nDelete' in elem_sing:
            elem_sing.remove('Verified\nEdit\nDelete')
        while 'Editr\nDelete' in elem_sing:
            elem_sing.remove('Edit\nDelete')
        while 'Not verified' in elem_sing:
            elem_sing.remove('Not verified')

        self.spf = []
        self.dkim = []
        for x in range(int(len(elem_sing) / 4)):
            self.spf.append(elem_sing[x * 4 + 2])
            self.dkim.append(elem_sing[x * 4 + 3])

        ################################### Qualidade e tamanho da base
        self.driver.get(URL + "/#Dashboard")

        try:
            elem = self.driver.find_elements_by_xpath("//img[@class='x-tool-close']")
            elem[0].click()
        except:
            pass

        xp(self.driver, 'empty', 'class', 'number ', 0)      ### preciso rever selector original é por class name, eu estou buscando o tag td
        self.cadast = self.query.attribute(0,'text')
        xp(self.driver, 'empty', 'class', 'quality_letter', 0)
        self.cadast = self.query.attribute(0,'text')
        elem = self.driver.find_element_by_class_name('quality_letter')
        self.quali = elem.text


    def specific_report(self,num_inter):
        def get_errors(driver):
            value_checker = ['Endereço inativo', 'Usuário desconhecido', 'Domínio desconhecido', 'Permanente']
            value_checker = [x[0:8] for x in value_checker]
            value_checker_en = ['Invalid address', 'Unknown user', 'Unknown domain', 'Permanent']
            value_checker_en = [x[0:8] for x in value_checker_en]

            xp(self.driver, 'text', 'empty', 'empty', 'list')
            elem = self.query.selector('list')

                # driver.find_elements_by_tag_name('text')
            error_list = [x.text for x in elem]
            error_list_checker = [x.text[0:8] for x in elem]
            values = []
            values_en = []

            for k in value_checker:
                if k in error_list_checker:
                    ind = error_list_checker.index(k)
                    value = error_list[ind]

                    values.append(float(value.split('(')[0].split(' ')[-2]))
                    values.append(float(value.split('(')[1].split('%')[0].replace(',', '.')))
                else:
                    values.append(0)
                    values.append(0)

            for k in value_checker_en:
                if k in error_list_checker:
                    ind = error_list_checker.index(k)
                    value = error_list[ind]

                    values_en.append(float(value.split('(')[0].split(' ')[-2]))
                    values_en.append(float(value.split('(')[1].split('%')[0].replace(',', '.')))
                else:
                    values_en.append(0)
                    values_en.append(0)
            if values_en.count(0) > values.count(0):
                return values
            elif values_en.count(0) < values.count(0):
                return values_en
            else:
                return values
        ###################################### Listas, erros, cancelamentos e denuncias
        URL = self.URL
        self.driver.get(URL + '/#CampaignList')

        # time.sleep(4)
        # elem = self.driver.find_elements_by_xpath("//input[@class='x-form-field x-form-empty-field x-form-text']")
        # elem[1].click()

        xp(self.driver,'input','class','x-form-field x-form-empty-field x-form-text',1)
        self.query.click(1)



        # time.sleep(3)
        # elem = self.driver.find_elements_by_xpath("//li[@class='x-boundlist-item']")

        xp(self.driver, 'li', 'class', 'x-boundlist-item', 'list')
        elem_list = self.query.selector('list')

        for x in elem_list:
            if x.get_attribute('textContent') == 'Interrompido':
                x.click()
                break
        time.sleep(1)

        self.driver.execute_script("a = document.getElementsByClassName('ac summary');"
                              "a.item(0).click();")

        # elem = self.driver.find_elements_by_xpath("//div[@class='status red']")
        # hover = ActionChains(self.driver).move_to_element(elem[num_inter])
        # hover.perform()
        # time.sleep(2)
        # elem = self.driver.find_elements_by_xpath("//li[@class='ac summary']")
        # elem[num_inter].click()
        # time.sleep(1)
        # elem = self.driver.find_elements_by_xpath("//td[@class = 'x-table-layout-cell ']")
        xp(self.driver, 'td', 'class', 'x-table-layout-cell ', 'list')
        elem = self.query.selector('list')

        elemstr = [str(x.text) for x in elem]
        lst = ['Lista de inclusão', 'Lista de exclusão', 'Segmentação']
        self.lista = []
        for x in lst:
            if x in elemstr:

                self.lista.append(elem[elemstr.index(x) + 1].text)
            else:
                self.lista.append('nenhuma')

        listus = self.lista[0:2]
        if listus.count('nenhuma') == 3:
            self.lista = []
            lst = ['Inclusion list', 'Exclusion list', 'Segmentation']
            for x in lst:
                if x in elemstr:

                    self.lista.append(elem[elemstr.index(x) + 1].text)
                else:
                    self.lista.append('nenhuma')

        xp(self.driver,htmltag='empty',htmlidentifier='class',htmlidentname='x-btn app-btn orange add x-box-item x-toolbar-item x-btn-default-toolbar-medium x-noicon x-btn-noicon x-btn-default-toolbar-medium-noicon',selector=0)
        self.driver.execute_script("a = document.getElementsByClassName('x-btn app-btn orange add x-box-item x-toolbar-item x-btn-default-toolbar-medium x-noicon x-btn-noicon x-btn-default-toolbar-medium-noicon');"
                              "a.item(0).click();")
        # elem = self.driver.find_element_by_xpath("//div[@class = 'x-btn app-btn orange add x-box-item x-toolbar-item x-btn-default-toolbar-medium x-noicon x-btn-noicon x-btn-default-toolbar-medium-noicon']")  ##elem.click()
        # elem.click()
        # time.sleep(2)

        # self.driver.execute_script("a = document.getElementsByClassName('x-btn app-btn orange add x-box-item x-toolbar-item x-btn-default-toolbar-medium x-noicon x-btn-noicon x-btn-default-toolbar-medium-noicon');"
        #                            "a.item(0).click();")
        #
        # elem = self.driver.find_elements_by_xpath("//input[@class='x-form-field x-form-empty-field x-form-text']")
        # hover = ActionChains(self.driver).move_to_element(elem[0])
        # hover.perform()
        # elem = self.driver.find_elements_by_xpath("//div[@class='status red']")
        # hover = ActionChains(self.driver).move_to_element(elem[num_inter])
        # hover.perform()
        # elem = self.driver.find_elements_by_xpath("//li[@class='ac report']")
        # elem[num_inter].click()
        self.driver.execute_script("a = document.getElementsByClassName('ac report');"
                              "a.item(0).click();")


        xp(self.driver, 'h1', 'empty', 'empty', 0)
        self.campanha = self.query.selector(0).text
        # print(elem.text)
        # print(elem.text)
        # print(elem.text)
        # try:
        #     self.campanha = elem.text.split('Sumário:')[1]
        # except:
        #     self.campanha = elem.text.split('Summary:')[1]
        # elem = self.driver.find_elements_by_class_name('x-form-trigger-wrap')
        # elem[4].click()
        # time.sleep(2)
        # Aba de erros
        # elem = self.driver.find_elements_by_class_name('x-grid-cell-inner')
        # elem[16].click()
        xp(self.driver, 'empty', 'class', 'x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable', 4)
        self.driver.execute_script("document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(4).click();")
        xp(self.driver, 'empty', 'class', 'x-tree-icon x-tree-icon-leaf', 14)
        self.driver.execute_script( "document.getElementsByClassName('x-tree-icon x-tree-icon-leaf').item(14).click();")

        self.erros = get_errors(self.driver)
        # Aba denúncias
        # elem = self.driver.find_elements_by_class_name('x-form-trigger-wrap')
        # elem[4].click()
        xp(self.driver, 'empty', 'class', 'x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable', 4)
        self.driver.execute_script("document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(4).click();")
        xp(self.driver, 'empty', 'class', 'x-tree-icon x-tree-icon-leaf', 10)
        self.driver.execute_script( "document.getElementsByClassName('x-tree-icon x-tree-icon-leaf').item(10).click();")

        # xp(self.driver,'empty','class','x-grid-cell-inner','list')
        # elem = self.query.selector('list')
        # # elem = self.driver.find_elements_by_class_name('x-grid-cell-inner')
        # ind = [x.text for x in elem]
        # try:
        #     elem[ind.index('Denúncias')].click()
        # except:
        #     elem[ind.index('Complaints')].click()
        # time.sleep(1)
        # elem = self.driver.find_elements_by_class_name('x-grid-cell-inner')
        xp(self.driver, 'empty', 'class', 'x-grid-cell-inner', 'list')
        elem = self.query.selector('list')
        a = [a.text for a in elem]
        self.denuncias = a.count('Denúncia de Spam')
        denuncias_en = a.count('Reporting Spam')
        denuncias_en = a.count('Reporting Spam')
        if self.denuncias != denuncias_en:
            if denuncias_en > self.denuncias:
                self.denuncias = denuncias_en
            elif self.denuncias > denuncias_en:
                pass
        # Aba cancelamento
        xp(self.driver, 'empty', 'class', 'x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable', 4)
        self.driver.execute_script("document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(4).click();")
        xp(self.driver, 'empty', 'class', 'x-tree-icon x-tree-icon-leaf', 9)
        self.driver.execute_script( "document.getElementsByClassName('x-tree-icon x-tree-icon-leaf').item(9).click();")

        xp(self.driver, 'empty', 'class', 'x-form-trigger-wrap', 4)
        self.query.click(4)
        # elem = self.driver.find_elements_by_class_name('x-form-trigger-wrap')
        # elem[4].click()
        xp(self.driver, 'empty', 'class', 'x-grid-cell-inner', 'list')
        elem = self.query.selector('list')
        # elem = self.driver.find_elements_by_class_name('x-grid-cell-inner')
        ind = [x.text for x in elem]
        try:
            elem[ind.index('Cancelamentos')].click()
        except:
            elem[ind.index('Cancellations')].click()

        xp(self.driver, 'empty', 'class', 'x-grid-cell-inner', 'list')
        elem = self.query.selector('list')
        # elem = self.driver.find_elements_by_class_name('x-grid-cell-inner')
        a = [a.text for a in elem]
        self.cance = 0
        for p in a:
            if '@' in p:
                self.cance = self.cance + 1
            elif 'excluído' in p:
                self.cance = self.cance + 1
            elif 'removed' in p:
                self.cance = self.cance + 1

    def del_seg(self):
        # ----------------------------- removendo segmentação antiga

        URL = self.URL
        self.driver.get(URL + '/#DataMining')


        xp(self.driver,'empty','class','x-form-field x-form-text x-form-empty-field',2)
        self.driver.execute_script(
            "document.getElementsByClassName('x-form-field x-form-text x-form-empty-field').item(2).value='(EMMr';")
        time.sleep(1)
        xp(self.driver, 'empty', 'class', 'x-trigger-index-1 x-form-trigger x-form-search-trigger x-form-trigger-last x-unselectable', 1)
        self.driver.execute_script(
            "document.getElementsByClassName('x-trigger-index-1 x-form-trigger x-form-search-trigger x-form-trigger-last x-unselectable').item(1).click();")
        # self.driver.execute_script(
        #     "document.getElementsByClassName('x-trigger-index-1 x-form-trigger x-form-search-trigger x-form-trigger-last x-unselectable').item(1).click();")
        # time.sleep(10)
        xp(self.driver, 'span', 'class', 'name', 'list')
        if not self.query.overrepeater:
            aaa = self.query.selector("list")
            print(aaa)
            print(len(aaa)*999)
        else:
            self.del_completa = True
            return 'sem analises completadas'

        jk = [x.get_attribute('innerHTML')[0:5] for x in aaa]
        print(jk)
        for x in jk:
            if x == '(EMMr':
                check = True
            else:
                check = False
                break

        if len(jk) == 0:
            check = False

        lll = jk.count('(EMMr')
        if check and lll!= 0:

            if jk.count('(EMMr') <= 6:
                for x in range(jk.count('(EMMr')):
                    xp(self.driver,'div','class','icon-del',0)
                    self.query.click(0)
                    xp(self.driver,'empty','class','x-btn-center',11)
                    self.query.click(11)


        self.del_completa = True


    def criar_seg(self,seg_num):
        ######## Criando segmentações
        URL = self.URL
        self.driver.get(URL + '/#DataMiningForm')

        NOME_SEG_LIST = ['(EMMr CI12M)','(EMMr CI6M)','(EMMr SI2010)']
        DIAS_SEG_LIST = [366,180]

        xp(self.driver, 'empty', 'class', 'x-form-field x-form-required-field x-form-text', 'list')
        self.driver.execute_script(
            "document.getElementsByClassName('x-form-field x-form-required-field x-form-text').item(0).value = '{0}';".format(NOME_SEG_LIST[seg_num]))
        time.sleep(0.5)
        self.driver.execute_script(    "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(0).click(); ")
        time.sleep(1)
        self.driver.execute_script("document.getElementsByClassName('x-grid-cell-inner ').item(0).click();")

        if seg_num <=1:
            self.driver.execute_script("document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(1).click(); "
                              "document.getElementsByClassName('x-grid-row x-grid-tree-node-leaf').item(16).click();"
                              "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(2).click();"
                              "document.getElementsByClassName('x-boundlist-item').item(2).click();")

            a = datetime.date.today() - datetime.timedelta(days=DIAS_SEG_LIST[seg_num])
            a = a.strftime("%d/%m/%Y")
            aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
            aaa[3].click()
            aaa[3].send_keys(a)
            self.driver.execute_script(
                "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(1).click(); ")
            time.sleep(0.5)
            aaa = self.driver.find_elements_by_xpath("//div[@class='x-btn x-box-item x-toolbar-item x-btn-default-toolbar-large x-noicon x-btn-noicon x-btn-default-toolbar-large-noicon']")
            aaa[0].click()

        else:
            self.driver.execute_script(
                "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(1).click(); "
                "document.getElementsByClassName('x-grid-row x-grid-tree-node-leaf').item(18).click();"
                "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(2).click();"
                "document.getElementsByClassName('x-boundlist-item').item(2).click();")


            aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
            aaa[3].click()
            aaa[3].send_keys('01/01/2010')

            self.driver.execute_script(
                "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(1).click(); ")

            time.sleep(0.5)
            aaa = self.driver.find_elements_by_xpath("//div[@class='x-btn x-box-item x-toolbar-item x-btn-default-toolbar-large x-noicon x-btn-noicon x-btn-default-toolbar-large-noicon']")
            aaa[0].click()
        # if seg_num == 0:
        #     bbb = self.driver.find_elements_by_xpath("//input[@class = 'x-form-field x-form-required-field x-form-text']")
        #     bbb[0].send_keys('(EMMr CI12M)')
        # if seg_num == 1:
        #     bbb = self.driver.find_elements_by_xpath("//input[@class = 'x-form-field x-form-required-field x-form-text']")
        #     bbb[0].send_keys('(EMMr CI6M)')
        # if seg_num == 2:
        #     bbb = self.driver.find_elements_by_xpath("//input[@class = 'x-form-field x-form-required-field x-form-text']")
        #     bbb[0].send_keys('(EMMr SI2010)')

        #
        #
        # xp(self.driver, 'td', 'class', 'x-form-trigger-input-cell', 0)
        # self.query.click(0)
        #
        #
        # xp(self.driver, 'div', 'class', 'x-grid-cell-inner ', 0)
        # self.query.click(0)
        #
        # xp(self.driver, 'td', 'class', 'x-form-trigger-input-cell', 1)
        # self.query.click(1)
        #
        # xxx = self.query.selector(1)
        #
        #
        # yyy = self.driver.find_elements_by_xpath("//button[@class = 'x-btn-center']")
        # hover1 = ActionChains(self.driver).move_to_element(yyy[10])
        # hover1.perform()
        # hover1 = ActionChains(self.driver).move_to_element(xxx)
        # hover1.perform()
        # yyy = self.driver.find_elements_by_xpath("//tr[@class = 'x-grid-row x-grid-tree-node-leaf']")
        # brk = 0
        # if seg_num ==0:
        #     while brk != 2:
        #         for l in yyy:
        #
        #             self.driver.execute_script("return arguments[0].scrollIntoView();", l)
        #             hover1 = ActionChains(self.driver).move_to_element(xxx)
        #             hover1.perform()
        #             hover1 = ActionChains(self.driver).move_to_element(yyy[int(-len(yyy) / 4)])
        #             hover1.perform()
        #             yyy = self.driver.find_elements_by_xpath("//tr[@class = 'x-grid-row x-grid-tree-node-leaf']")
        #
        #             for x in yyy:
        #
        #                 if x.text == 'Com (visualizações e cliques)':
        #                     x.click()
        #                     brk = 2
        #                     break
        #                 elif x.text == 'With (impressions and clicks)':
        #                     x.click()
        #                     brk = 2
        #                     break
        #
        #             if brk == 2:
        #                 break
        #     time.sleep(2)
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[2].click()
        #     aaa = self.driver.find_elements_by_xpath("//li[@class = 'x-boundlist-item']")
        #     aaa[1].click()
        #     a = datetime.date.today() - datetime.timedelta(days=365)
        #     a = a.strftime("%d/%m/%Y")
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[3].click()
        #     aaa[3].send_keys(a)
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[3].click()
        #     time.sleep(3)
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[0].click()
        #     aaa = self.driver.find_elements_by_xpath("//div[@class='x-btn x-box-item x-toolbar-item x-btn-default-toolbar-large x-noicon x-btn-noicon x-btn-default-toolbar-large-noicon']")
        #     aaa[0].click()


        ######## Criando segmentação (EMMr CI6M)
        # elif seg_num ==1:
        #     while brk != 2:
        #         for l in yyy:
        #             self.driver.execute_script("return arguments[0].scrollIntoView();", l)
        #             # hover = ActionChains(driver).move_to_element(l)
        #             # hover.perform()
        #             hover = ActionChains(self.driver).move_to_element(xxx[1])
        #             hover.perform()
        #             hover = ActionChains(self.driver).move_to_element(yyy[int(-len(yyy) / 4)])
        #             hover.perform()
        #             yyy = self.driver.find_elements_by_xpath("//tr[@class = 'x-grid-row x-grid-tree-node-leaf']")
        #             for x in yyy:
        #                 # if x.text == 'Com (visualizações e cliques)':
        #                 if x.text == 'Com (visualizações e cliques)':
        #                     x.click()
        #                     brk = 2
        #                     break
        #                 elif x.text == 'With (impressions and clicks)':
        #                     x.click()
        #                     brk = 2
        #                     break
        #             if brk == 2:
        #                 break
        #     brk = 0
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[2].click()
        #     aaa = self.driver.find_elements_by_xpath("//li[@class = 'x-boundlist-item']")
        #     aaa[1].click()
        #     a = datetime.date.today() - datetime.timedelta(days=180)
        #     a = a.strftime("%d/%m/%Y")
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[3].click()
        #     aaa[3].send_keys(a)
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[3].click()
        #     time.sleep(3)
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[0].click()
        #     aaa = self.driver.find_elements_by_xpath(
        #         "//div[@class='x-btn x-box-item x-toolbar-item x-btn-default-toolbar-large x-noicon x-btn-noicon x-btn-default-toolbar-large-noicon']")
        #     aaa[0].click()

        #
        # if seg_num==2:
        #     while brk != 2:
        #         for l in yyy:
        #             self.driver.execute_script("return arguments[0].scrollIntoView();", l)
        #
        #             hover = ActionChains(self.driver).move_to_element(xxx[1])
        #             hover.perform()
        #             hover = ActionChains(self.driver).move_to_element(yyy[int(-len(yyy) / 4)])
        #             hover.perform()
        #             yyy = self.driver.find_elements_by_xpath("//tr[@class = 'x-grid-row x-grid-tree-node-leaf']")
        #             for x in yyy:
        #
        #                 if x.text == 'Sem':
        #                     x.click()
        #                     brk = 2
        #                     break
        #                 elif x.text == 'Without':
        #                     x.click()
        #                     brk = 2
        #                     break
        #             if brk == 2:
        #                 break
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[2].click()
        #     aaa = self.driver.find_elements_by_xpath("//li[@class = 'x-boundlist-item']")
        #     aaa[1].click()
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[3].click()
        #     aaa[3].send_keys('01/01/2010')
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[3].click()
        #     time.sleep(3)
        #     aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
        #     aaa[0].click()
        #     time.sleep(1)
        #     aaa = self.driver.find_elements_by_xpath("//div[@class='x-btn x-box-item x-toolbar-item x-btn-default-toolbar-large x-noicon x-btn-noicon x-btn-default-toolbar-large-noicon']")
        #     aaa[0].click()

    def seg_values(self):
        URL = self.URL
        self.driver.get(URL + '/#DataMining')

        xp(self.driver,'empty','class','x-form-field x-form-text x-form-empty-field',2)
        self.driver.execute_script("document.getElementsByClassName('x-form-field x-form-text x-form-empty-field').item(2).value='(EMMr'")
        time.sleep(0.5)
        self.driver.execute_script("document.getElementsByClassName('x-trigger-index-1 x-form-trigger x-form-search-trigger x-form-trigger-last x-unselectable').item(1).click()")
        time.sleep(0.5)
        self.driver.execute_script("document.getElementsByClassName('x-trigger-index-1 x-form-trigger x-form-search-trigger x-form-trigger-last x-unselectable').item(1).click()")

        xp(self.driver, 'span', 'class', 'name', 'list')
        aaa = self.query.selector('list')
        # aaa = self.driver.find_elements_by_xpath("//span[@class = 'name']")
        jkk = [o.get_attribute('innerHTML') for o in aaa]
        jk = [u.get_attribute('innerHTML')[0:5] for u in aaa]
        for x in jk:
            if x == '(EMMr':
                check = True
            else:
                check = False
                break
        a = []
        for x in range(3):
            if check:
                xp(self.driver, 'empty', 'class', 'icon-total icon-open-node', x)
                self.driver.execute_script("document.getElementsByClassName('icon-total icon-open-node').item({0}).click();".format(x))
                xp(self.driver, 'empty', 'class', 'x-grid-cell-inner ', 0)
                self.driver.execute_script("document.getElementsByClassName('x-grid-cell-inner ').item(0).click();")
                xp(self.driver, 'empty', 'class', 'x-btn-center', 11)
                self.driver.execute_script("document.getElementsByClassName('x-btn-center').item(11).click();")
                xp(self.driver, 'span', 'class', 'number-blue', 0)
                aaa = self.query.selector(0)
                try:
                    a.append(aaa[0].get_attribute('innerHTML'))
                except IndexError:
                    a.append('null')
                self.driver.execute_script("document.getElementsByClassName('x-tool-close').item(0).click();")

        self.segmen = ['a', 'a', 'a']
        for c in jkk:
            if c == '(EMMr CI6M)':
                self.segmen[0] = a[jkk.index(c)]
            elif c == '(EMMr CI12M)':
                self.segmen[1] = a[jkk.index(c)]
            elif c == '(EMMr SI2010)':
                self.segmen[2] = a[jkk.index(c)]


############################ OLD CODE

                # this = Analise()
# print(this.aaa)
# this.login()
# this.consolidado()



# driver.get(URL + "/#Report/Consolidated")
# time.sleep(10)
# elem = table_get(driver)
#
# try:
#     visua.append(table_value(elem, "total de visualizações"))
#     clicks.append(table_value(elem, "total de cliques"))
#
# except:
#
#     print('no data 1')
# try:
#     visua.append(table_value(elem, "total views"))
#     clicks.append(table_value(elem, "total clicks"))
#
# except:
#
#     print('no data 1')
#
#

#
#
#
# from selenium import webdriver
#
#
# driver = webdriver.Firefox()
# driver.get("http://somedomain/url_that_delays_loading")









# driver.execute_script("aaa = document.getElementsByName('login').item(0); aaa.value = 'andre.duarte/admin'")
# driver.execute_script("aaa = document.getElementById('pass'); aaa.text = '75KZd55n'")



#############################DUMP

# WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'x-form-trigger-wrap')))
# elem = self.driver.find_element_by_class_name('x-form-trigger-wrap')
# WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@class='x-form-trigger-wrap']")))
# elem = self.driver.find_element_by_class_name('x-form-trigger-wrap')