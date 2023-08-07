from typing import Type
from bs4 import BeautifulSoup as bs
import requests as r
from dataclasses import dataclass, field
from threading import Thread
import os

_WW_CMD='wsl wget -nv'
DOWNLOAD_FOLDER=os.environ.get('WWWGETPY_DOWNLOAD_FOLDER','./')

@dataclass
class ElementBuilder:
    domain: str
    name: str
    parent_path: str
    complete_path: str = field(init=False)
    complete_url: str = field(init=False)
    
    def __post_init__(self) -> None:
        self.complete_path=f"{self.parent_path}/{self.name}"
        self.complete_url=f"{self.domain}/{self.complete_path}"
        
    def is_folder(self):
        name=self.name
        is_folder_v=True
        if len(name.split('.'))>=2:
            is_folder_v=False
        return is_folder_v
    
    def build_element(self):
        if self.is_folder():
            return Folder(self.domain,self.name,
                            self.parent_path,
                            self.complete_path,
                            self.complete_url)
        
        else:
            return File(self.domain,self.name,
                            self.parent_path,
                            self.complete_path,
                            self.complete_url)
    
    def run_element(self):
        if self.is_folder():
            print(f'***FOLDER \n {self.complete_path} folder is going to be created')
            Folder(self.domain,self.name,
                            self.parent_path,
                            self.complete_path,
                            self.complete_url).download()
        else:
            print(f'---FILE \n {self.name} is going to be download')
            File(self.domain,self.name,
                            self.parent_path,
                            self.complete_path,
                            self.complete_url).download()


@dataclass
class Folder(ElementBuilder):
    complete_path: str # This address is needed to know the local destination
    complete_url: str # This address is needed to know the web source
    
    def run_source(self):
        print(f'A new Source was created for {self.name}')
        Source(domain=self.domain,
               path=self.complete_path).run_all_elements()
        
    def download(self):
        try:
            # Run a source for this folder
            Thread(target=self.run_source).start()
            exec_msg=f'It was possible to manage {self.name}.'
            print(exec_msg)
         
        except Exception as e:
            exec_msg=f'It WASNT possible to manage {self.name} because of {str(e)}.'
            print(exec_msg)
        


@dataclass
class File(ElementBuilder):
    complete_path: str # This address is needed to know the local destination
    complete_url: str # This address is needed to know the web source
    
    def download(self):
        try:
            os.system(f'{_WW_CMD} {self.complete_url} -P {DOWNLOAD_FOLDER}\{self.parent_path}')
            exec_msg=f'It was possible to get the file {self.name} in {self.parent_path}.'
            print(self.complete_path)
        except Exception as e:
            exec_msg=f'It WASNT possible to get the file {self.name} because of {str(e)}.'
        
        return exec_msg

@dataclass
class Source:
    domain: str = os.environ.get('WWWGETPY_DOMAIN') # The domain could not change
    path: str = None # The path must change to be recursive, by default the class won't be init
    url: str = field(init=False)
    
    def __post_init__(self):
        if None in (self.domain,self.path):
            raise ValueError(f'None is not a valid value, check: \n- domain: {self.domain} \n- path: {self.path}')
        
        self.url=f"{self.domain}/{self.path}"
    
    def get_all_elements(self):
        str_html=r.get(self.url).text
        raw_html=bs(str_html)
        all_elements_names=[a['href'] for a in raw_html.find_all('a')
                                        if "?" not in a['href']
                                        and "Parent Directory" not in a.text
                                        ]
        
        all_elements=[]
        for e in all_elements_names:
            all_elements.append(ElementBuilder(
                                domain=self.domain,
                                name=e,parent_path=self.path
                                ).build_element())
        return all_elements
    
    def run_all_elements(self) -> None:
        str_html=r.get(self.url).text
        raw_html=bs(str_html)
        all_elements_names=[a['href'] for a in raw_html.find_all('a') if "?" not in a['href']]
        print(f"These are all the elements:\n")
        for e in all_elements_names: print(f"    - {e}\n")
        
        for e in all_elements_names:
            ElementBuilder(domain=self.domain,
                           name=e,parent_path=self.path
                           ).run_element()

@dataclass
class Manager():
    domain: str = os.environ.get('WWWGETPY_DOMAIN') # 'http://google.com'
    path: str = os.environ.get('WWWGETPY_PATH') # 'search'
    
    def __post_init__(self):
        if None in (self.domain,self.path):
            raise ValueError(f'None is not a valid value, check: \n- domain: {self.domain} \n- path: {self.path}')
        
        self.s = Source(domain=self.domain,path=self.path)
    
    def download_all_files(self) -> None:
        all_elem=self.s.get_all_elements()
        for e in all_elem: e.download()

if __name__=='__main__':
    m=Manager().download_all_files()

