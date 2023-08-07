from __future__ import annotations
from typing import List
import requests
import pandas as pd
import json
import shortuuid
from recordclass import recordclass

URL = "https://api.therichview.com"

import warnings

import io

import mergedeep


# Moved the RichViewSession class to the top as it is used in other classes
class RichViewSession:
    """
    A class used to represent a RichView Session.

    Attributes
    ----------
    headers : dict
        a dictionary containing the access token
    token : str
        the access token for the session

    Methods
    -------
    _get(url_ending)
        Sends a GET request to the specified URL.
    _post(url_ending, body)
        Sends a POST request to the specified URL with the provided body.
    _delete(url_ending)
        Sends a DELETE request to the specified URL.
    _put(url_ending, body)
        Sends a PUT request to the specified URL with the provided body.
    authenticate_with_password(email, password)
        Authenticates the user with the provided email and password.
    get_reports()
        Retrieves all the RichView reports in the user's account.
    get_report(report_id)
        Retrieves a specific report using its ID.
    create_report(report)
        Creates a new report.
    delete_report(report_id)
        Deletes a specific report using its ID.
    """

    def __init__(self, token: str):
        self.headers = {'x-access-token': token}
        self.token = token

    def _get(self, url_ending: str):
        url = f"{URL}/api/{url_ending}"
        response = requests.get(url, headers=self.headers)
        return response

    def _post(self, url_ending, body: dict):
        url = f"{URL}/api/{url_ending}"
        response = requests.post(url, headers=self.headers, json=body)
        return response

    def _delete(self, url_ending: str):
        url = f"{URL}/api/{url_ending}"
        response = requests.delete(url, headers=self.headers)
        return response

    def _put(self, url_ending, body: dict):
        url = f"{URL}/api/{url_ending}"
        response = requests.put(url, headers=self.headers, json=body)
        return response

    @classmethod
    def authenticate_with_password(cls, email: str, password: str) -> RichViewSession:
        url_ending = f"login"
        body = {"email": email, "password": password}
        session = cls('tmp_token')
        response = session._post(url_ending, body=body)
        if not response.ok:
            raise Exception(
                f'Authentication failed: {response.status_code} {response.text}: {response.status_code} {response.text}'
            )
        token = response.json()['jwt_token']
        return cls(token)

    def get_reports(self) -> list:
        url_ending = f"reports"
        response = self._get(url_ending)
        if not response.ok:
            raise Exception(f'Failed to get reports: {response.status_code} {response.text}')
        return [
            RichViewReport(id=report_dict['id'],
                           title=report_dict['title'],
                           lastEdited=report_dict['lastEdited'],
                           blocks=report_dict['content']['blocks'],
                           session=self) for report_dict in response.json()['result']
        ]

    def get_report(self, report_id) -> RichViewReport:
        url_ending = f"report/{report_id}"
        response = self._get(url_ending)
        if not response.ok:
            raise Exception(f'Failed to get report: {response.status_code} {response.text}')
        return RichViewReport(**response.json()['result'],
                              blocks=response.json()['result']['content']['blocks'],
                              session=self)

    def create_report(self, report: RichViewReport) -> RichViewReport:
        url_ending = f"report"
        body = {
            "title": report.title,
            "content": {
                "blocks": [block._asdict() for block in report.blocks]
            }
        }
        response = self._post(url_ending, body=body)
        if not response.ok:
            raise Exception(f'Failed to create report: {response.status_code} {response.text}')
        return RichViewReport(**response.json()['result'],
                              blocks=response.json()['result']['content']['blocks'],
                              session=self.session)

    def delete_report(self, report_id) -> bool:
        url_ending = f"report/{report_id}"
        response = self._delete(url_ending)
        if not response.ok:
            raise Exception(f'Failed to delete report: {response.status_code} {response.text}')
        return True


class RichViewBlock:
    """
    A class used to represent a RichView Block.

    Attributes
    ----------
    report_id : str
        the ID of the report the block belongs to
    block_id : str
        the ID of the block
    block_type : str
        the type of the block (e.g., 'chart', 'image', 'header', etc.)
    data : dict
        the data contained in the block
    session : RichViewSession
        the session the block belongs to
    synced_with_server : bool
        a flag indicating whether the block is synced with the server

    Methods
    -------
    update_block(**kwargs)
        Updates the block with the provided keyword arguments.
    update_online_version()
        Updates the online version of the block.
    get_online_version()
        Retrieves the online version of the block.
    _asdict(assign_id=True)
        Returns a dictionary representation of the block.
    """

    def __init__(self,
                 report_id: str,
                 type: str,
                 data: dict,
                 session: RichViewSession,
                 id: str = None):
        if report_id is None:
            warnings.warn('Blocks Report ID is None, block can not be synced directlywith server')
        self.report_id = report_id
        self.block_id = id
        self.block_type = type
        self.data = data
        self.session = session
        self.synced_with_server = True

    def update_block(self, **kwargs):
        url_ending = f"/report/{self.report_id}/block/{self.block_id}"
        for kwarg in kwargs.keys():
            assert hasattr(
                self.data, kwarg
            ), f'Property {kwarg} is not valid for block type {self.block_type}, valid properties are {self.data._fields}'
        new_data = mergedeep.merge({}, self.data._asdict(), kwargs)
        body = {"type": self.block_type, "data": new_data, "id": f"{self.block_id}"}
        response = self.session._put(url_ending, body=body)
        if not response.ok:
            raise Exception(f'Failed to update block: {response.status_code} {response.text}')

        self.synced_with_server = False

        return _convert_block(block_dict=response.json()['result'],
                              report_id=self.report_id,
                              session=self.session)

    def update_online_version(self):
        self.update_block(**self.data._asdict())
        self.synced_with_server = True

    def get_online_version(self) -> RichViewBlock:
        if self.synced_with_server:
            warnings.warn('Online version is already synced with local version')

        url_ending = f"/report/{self.report_id}/block/{self.block_id}"
        response = self.session._get(url_ending)
        if not response.ok:
            raise Exception(f'Failed to get online version: {response.status_code} {response.text}')
        self.synced_with_server = True
        self.__init__(**response.json()['result'],
                      blocks=response.json()['result']['content']['blocks'],
                      session=self.session)
        return self

    def _asdict(self, assign_id=True):
        if assign_id:
            if self.block_id is None:
                self.block_id = shortuuid.ShortUUID().random(length=10)
        return {"type": self.block_type, "data": self.data._asdict(), "id": self.block_id}


class ChartBlock(RichViewBlock):
    """
    A class used to represent a Chart Block.

    Parameters
    ----------
    chart_options_dict : dict
        a dictionary containing the chart options
    title : str
        the title of the chart

    Methods
    -------
    get_data()
        Retrieves the data of the chart.
    set_data(df)
        Sets the data of the chart.
    set_title(title)
        Sets the title of the chart.
    get_options()
        Retrieves the chart options.
    update_options(force=False, **kwargs)
        Updates the chart options.
    """
    ChartBlockData = recordclass('ChartBlockData', ['chartOptions'])

    def __init__(self,
                 report_id: str,
                 chartOptions: str,
                 session: RichViewSession,
                 id: str = None,
                 **kwargs):
        data = {'chartOptions': chartOptions}
        data = self.ChartBlockData(**data)
        super().__init__(report_id=report_id, id=id, type='chart', data=data, session=session)
        self.chart_options_dict: dict = json.loads(self.data.chartOptions)

        self.title = self.chart_options_dict.get('title', {}).get('text', '')

    def get_data(self) -> pd.DataFrame:
        url_ending = f"/report/{self.report_id}/chart/{self.block_id}/data"
        response = self.session._get(url_ending)
        assert response.ok
        data = response.json()['result']['csvdata']
        df = pd.read_csv(io.StringIO(data))

        # make the first column the index
        df.set_index(df.columns[0], inplace=True)

        # check if DataFrame has ' | ' in index and then split them into multiindex
        try:
            if ' | ' in df.index[0]:
                df.index = pd.MultiIndex.from_tuples(df.index.str.split(' | ',
                                                                        regex=False).tolist(),
                                                     names=df.index.name.split(' | '))
        except TypeError:
            pass

        array_columns = self.check_for_array_columns(df)
        if len(array_columns) > 0:
            df = self.convert_array_columns(df, array_columns)
        return df

    @staticmethod
    def convert_array_columns(df, array_columns):
        for column in array_columns:
            df.loc[:, column] = df.loc[:, column].apply(
                lambda list_str:
                [int(x) if x.isdigit() else float(x) for x in list_str.strip('[]').split(',')])
        return df

    @staticmethod
    def check_for_array_columns(df):
        are_collumns_arrays = df.iloc[0, :].apply(lambda x: isinstance(x, str) and '[' in x)
        array_columns = df.columns[are_collumns_arrays]
        return array_columns

    def set_data(self, df: pd.DataFrame) -> ChartBlock:
        if not isinstance(df, pd.DataFrame):
            raise Exception('Data must be a pandas DataFrame')

        # check if DataFrame has a single index 'Category' or multiindex 'Category X', 'Category Y'
        if not (df.index.name == 'Category' or
                (isinstance(df.index, pd.MultiIndex)
                 and list(df.index.names) == ['Category X', 'Category Y'])):
            raise Exception(
                'DataFrame index must be either "Category" or Multiindex ["Category X", "Category Y"]'
            )

        # check if DataFrame has multiindex and then join them together with " | "
        if isinstance(df.index, pd.MultiIndex):
            old_names = df.index.names
            df.index = df.index.map(' | '.join)
            df.index.name = ' | '.join(old_names)

        url_ending = f"/report/{self.report_id}/chart/{self.block_id}/data"
        body = {"csvdata": df.to_csv()}
        response = self.session._put(url_ending, body=body)
        if not response.ok:
            raise Exception(f'Failed to set chart data: {response.status_code} {response.text}')
        self.synced_with_server = False
        chart_options_string = response.json()['result']['chartOptions']

        return ChartBlock(report_id=self.report_id,
                          id=self.block_id,
                          chartOptions=chart_options_string,
                          session=self.session)

    def set_title(self, title: str) -> ChartBlock:
        self.title = title
        url_ending = f"/report/{self.report_id}/chart/{self.block_id}/title"
        body = {"title": title}
        response = self.session._put(url_ending, body=body)
        if not response.ok:
            raise Exception(f'Failed to set chart title: {response.status_code} {response.text}')
        return ChartBlock(report_id=self.report_id,
                          session=self.session,
                          id=self.block_id,
                          chartOptions=response.json()['result'])

    def get_options(self) -> dict:
        return self.chart_options_dict

    def update_options(self, force: bool = False, **kwargs) -> ChartBlock:
        """update_options _summary_

        Args:
            force (bool, optional): Allows for creation of new properties. Defaults to False.
            kwargs: chart options to update

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        url_ending = f"/report/{self.report_id}/chart/{self.block_id}"

        if not force:
            check_if_all_properties_exist(kwargs, self.chart_options_dict)

        new_options = mergedeep.merge({}, self.chart_options_dict, kwargs)
        body = {"data": {"chartOptions": json.dumps(new_options)}}
        response = self.session._put(url_ending, body=body)
        if not response.ok:
            raise Exception(
                f'Failed to update chart options: {response.status_code} {response.text}')
        self.synced_with_server = False
        return _convert_block(block_dict=response.json()['result'],
                              report_id=self.report_id,
                              session=self.session)

    def __repr__(self) -> str:
        return f"ChartBlock(id={self.block_id}, title={self.title})"


class ImageBlock(RichViewBlock):
    """
    A class used to represent an Image Block.

    Parameters
    ----------
    report_id : str
        The ID of the report the image block belongs to
    file : str
        The file of the image block
    withBorder : bool
        A flag indicating whether the image block has a border
    stretched : bool
        A flag indicating whether the image block is stretched
    withBackground : bool
        A flag indicating whether the image block has a background
    session : RichViewSession
        The session the image block belongs to
    caption : str, optional
        The caption of the image block (default is '')
    id : str, optional
        The ID of the image block (default is None)

    Methods
    -------
    __repr__()
        Returns a string representation of the image block
    """

    ImageBlockData = recordclass('ImageBlockData',
                                 ['file', 'caption', 'withBorder', 'stretched', 'withBackground'])

    def __init__(self,
                 report_id: str,
                 file: str,
                 withBorder: bool,
                 stretched: bool,
                 withBackground: bool,
                 session: RichViewSession,
                 caption: str = '',
                 id: str = None):
        """

        """
        data = self.ImageBlockData(file=file,
                                   caption=caption,
                                   withBorder=withBorder,
                                   stretched=stretched,
                                   withBackground=withBackground)
        super().__init__(report_id=report_id, id=id, type='image', data=data, session=session)

    def __repr__(self):
        return f"ImageBlock(id={self.block_id}, caption={self.data.caption})"


class HeaderBlock(RichViewBlock):
    HeaderBlockData = recordclass('HeaderBlockData', ['text', 'level'])
    """
    A class used to represent a Header Block.
    Parameters
    ----------
    report_id : str
        The ID of the report the header block belongs to
    text : str
        The text of the header block
    level : int
        The level of the header block
    session : RichViewSession
        The session the header block belongs to
    id : str, optional
        The ID of the header block (default is None)

    Methods
    -------
    __repr__()
        Returns a string representation of the header block
    """

    def __init__(self,
                 report_id: str,
                 text: str,
                 level: int,
                 session: RichViewSession,
                 id: str = None):
        """

        """
        data = self.HeaderBlockData(text=text, level=level)
        super().__init__(report_id=report_id, id=id, type='header', data=data, session=session)

    def __repr__(self):
        return f"HeaderBlock(id={self.block_id}, text={self.data.text[:10]}...)"


class ParagraphBlock(RichViewBlock):
    """
    A class used to represent a Paragraph Block.
    Parameters
    ----------
    report_id : str
        The ID of the report the paragraph block belongs to
    text : str
        The text of the paragraph block
    session : RichViewSession
        The session the paragraph block belongs to
    id : str, optional
        The ID of the paragraph block (default is None)

    Methods
    -------
    __repr__()
        Returns a string representation of the paragraph block
    """
    ParagraphBlockData = recordclass('ParagraphBlockData', ['text'])

    def __init__(self, report_id: str, text: str, session: RichViewSession, id: str = None):
        """

        """
        data = self.ParagraphBlockData(text=text)
        super().__init__(report_id=report_id, id=id, type='paragraph', data=data, session=session)

    def __repr__(self):
        return f"ParagraphBlock(id={self.block_id}, text={self.data.text[:10]}...)"


class EmbedBlock(RichViewBlock):
    """
    A class used to represent an Embed Block.

    Parameters
    ----------
    report_id : str
        The ID of the report the embed block belongs to
    service : str
        The service of the embed block
    source : str
        The source of the embed block
    embed : str
        The embed of the embed block
    width : int
        The width of the embed block
    height : int
        The height of the embed block
    session : RichViewSession
        The session the embed block belongs to
    caption : str, optional
        The caption of the embed block (default is '')
    id : str, optional
        The ID of the embed block (default is None)

    Methods
    -------
    __repr__()
        Returns a string representation of the embed block

    """
    EmbedBlockData = recordclass('EmbedBlockData',
                                 ['service', 'source', 'embed', 'width', 'height', 'caption'])

    def __init__(self,
                 report_id: str,
                 service: str,
                 source: str,
                 embed: str,
                 width: int,
                 height: int,
                 session: RichViewSession,
                 caption: str = '',
                 id: str = None):
        """

        """
        data = self.EmbedBlockData(service=service,
                                   source=source,
                                   embed=embed,
                                   width=width,
                                   height=height,
                                   caption=caption)
        super().__init__(report_id=report_id, id=id, type='embed', data=data, session=session)

    def __repr__(self):
        return f"EmbedBlock(id={self.block_id}, service={self.data.service})"


class TableBlock(RichViewBlock):
    """
    A class used to represent a Table Block.

    Methods
    -------
    __repr__()
        Returns a string representation of the table block
    """
    TableBlockData = recordclass('TableBlockData', ['content', 'withHeadings'])

    def __init__(self,
                 report_id: str,
                 content: list,
                 withHeadings: bool,
                 session: RichViewSession,
                 id: str = None):
        """
        Attributes
        ----------
        report_id : str
            The ID of the report the table block belongs to
        content : list
            The content of the table block
        withHeadings : bool
            A flag indicating whether the table block has headings
        session : RichViewSession
            The session the table block belongs to
        id : str, optional
            The ID of the table block (default is None)
        """
        data = self.TableBlockData(content=content, withHeadings=withHeadings)
        super().__init__(report_id=report_id, id=id, type='table', data=data, session=session)

    def __repr__(self):
        return f"TableBlock(id={self.block_id})"


class CodeBlock(RichViewBlock):
    """
    A class used to represent a Code Block.

    Parameters
    ----------
    report_id : str
        The ID of the report the code block belongs to
    code : str
        The code of the code block
    language : str
        The language of the code block
    showlinenumbers : bool
        A flag indicating whether the code block shows line numbers
    session : RichViewSession
        The session the code block belongs to
    id : str, optional
        The ID of the code block (default is None)

    Methods
    -------
    __repr__()
        Returns a string representation of the code block
    """
    CodeBlockData = recordclass('CodeBlockData', ['code', 'language', 'showlinenumbers'])

    def __init__(self,
                 report_id: str,
                 code: str,
                 language: str,
                 showlinenumbers: bool,
                 session: RichViewSession,
                 id: str = None):
        """

        """
        data = self.CodeBlockData(code=code, language=language, showlinenumbers=showlinenumbers)
        super().__init__(report_id=report_id, id=id, type='code', data=data, session=session)

    def __repr__(self):
        return f"CodeBlock(id={self.block_id}, language={self.data.language})"


class ListBlock(RichViewBlock):
    """
    A class used to represent a List Block.

    Parameters
    ----------
    report_id : str
        The ID of the report the list block belongs to
    style : str
        The style of the list block
    items : list
        The items of the list block
    session : RichViewSession
        The session the list block belongs to
    id : str, optional
        The ID of the list block (default is None)

    Methods
    -------
    __repr__()
        Returns a string representation of the list block
    """
    ListBlockData = recordclass('ListBlockData', ['style', 'items'])

    def __init__(self,
                 report_id: str,
                 style: str,
                 items: list,
                 session: RichViewSession,
                 id: str = None):
        """

        """
        data = self.ListBlockData(style=style, items=items)
        super().__init__(report_id=report_id, id=id, type='list', data=data, session=session)

    def __repr__(self):
        return f"ListBlock(id={self.block_id}, style={self.data.style})"


def _convert_block(block_dict: dict, session: RichViewSession, report_id) -> RichViewBlock:
    if isinstance(block_dict, RichViewBlock):
        return block_dict
    block_type = block_dict['type']
    block_id = block_dict.get('id', block_dict.get('block_id', None))
    if block_type == 'image':
        return ImageBlock(report_id=report_id,
                          id=block_dict['id'],
                          **block_dict['data'],
                          session=session)
    elif block_type == 'header':
        return HeaderBlock(report_id=report_id,
                           id=block_dict['id'],
                           **block_dict['data'],
                           session=session)
    elif block_type == 'paragraph':
        return ParagraphBlock(report_id=report_id,
                              id=block_dict['id'],
                              **block_dict['data'],
                              session=session)
    elif block_type == 'embed':
        return EmbedBlock(report_id=report_id,
                          id=block_dict['id'],
                          **block_dict['data'],
                          session=session)
    elif block_type == 'table':
        return TableBlock(report_id=report_id,
                          id=block_dict['id'],
                          **block_dict['data'],
                          session=session)
    elif block_type == 'code':
        return CodeBlock(report_id=report_id,
                         id=block_dict['id'],
                         **block_dict['data'],
                         session=session)
    elif block_type == 'list':
        return ListBlock(report_id=report_id,
                         id=block_dict['id'],
                         **block_dict['data'],
                         session=session)
    elif block_type == 'chart':
        return ChartBlock(report_id=report_id,
                          id=block_dict['id'],
                          **block_dict['data'],
                          session=session)

    raise ValueError(f'Unknown block type: {block_type}')


class RichViewReport:
    """
    A class used to represent a RichView Report.

    Attributes
    ----------
    title : str
        the title of the report
    session : RichViewSession
        the session the report belongs to
    synced_with_server : bool
        a flag indicating whether the report is synced with the server
    lastEdited : str
        the last edited timestamp of the report
    report_id : str
        the ID of the report
    blocks : list
        a list of blocks in the report

    Methods
    -------
    duplicate()
        Duplicates the report.
    send(email_receiving_editor)
        Sends the report to the specified email.
    query(type, data)
        Queries the report for blocks of a specific type and data.
    set_title(title)
        Sets the title of the report.
    get_charts()
        Retrieves all the charts in the report.
    get_chart(chart_id)
        Retrieves a specific chart using its ID.
    get_block(block_id)
        Retrieves a specific block using its ID.
    get_blocks()
        Retrieves all the blocks in the report.
    add_block(block)
        Adds a block to the report.
    delete_block(block_id)
        Deletes a specific block using its ID.
    update_online_version()
        Updates the online version of the report.
    get_online_version()
        Retrieves the online version of the report.
    """

    def __init__(self,
                 title: str,
                 blocks: list,
                 session: RichViewSession,
                 id: str = None,
                 lastEdited: str = None,
                 **kwargs):
        self.title = title
        self.session = session
        self.synced_with_server = True
        self.lastEdited = lastEdited
        self.report_id = id
        self.blocks: list[RichViewBlock] = [
            _convert_block(block, session, report_id=self.report_id) for block in blocks
        ]

    def __repr__(self):
        return f"RichViewReport(id={self.report_id}, title={self.title})"

    def duplicate(self) -> RichViewReport:
        url_ending = f"/report"
        body = {
            "title": self.title + ' (Copy)',
            "content": {
                'blocks': [block._asdict() for block in self.blocks]
            }
        }
        response = self.session._post(url_ending, body=body)
        if not response.ok:
            raise Exception(f'Failed to duplicate report: {response.status_code} {response.text}')
        self.synced_with_server = False
        return RichViewReport(**response.json()['result'],
                              blocks=response.json()['result']['content']['blocks'],
                              session=self.session)

    def send(self, email_receiving_editor: str) -> bool:
        url_ending = f"report/{self.report_id}/send"
        data = {'new_author_id': email_receiving_editor}
        response = self.session._post(url_ending, body=data)
        if not response.ok:
            raise Exception(f'Failed to send report: {response.status_code} {response.text}')
        return True

    def query(self, type: str, data: str) -> List[RichViewBlock]:
        return [block for block in self.blocks if block.type == type and block.data == data]

    def set_title(self, title: str) -> RichViewReport:
        self.title = title
        url_ending = f"report/{self.report_id}"
        body = {"title": title}
        response = self.session._put(url_ending, body=body)
        if not response.ok:
            raise Exception(
                f'Failed to update report title: {response.status_code} {response.text}')
        self.synced_with_server = False
        return RichViewReport(**response.json()['result'],
                              blocks=response.json()['result']['content']['blocks'],
                              session=self.session)

    def get_charts(self) -> List[ChartBlock]:
        return [block for block in self.blocks if isinstance(block, ChartBlock)]

    def get_chart(self, chart_id: str) -> ChartBlock:
        chart = next((block for block in self.blocks
                      if block.block_id == chart_id and isinstance(block, ChartBlock)), None)
        if chart is None:
            raise Exception(f'Chart with id {chart_id} not found')
        return chart

    def get_block(self, block_id: str) -> RichViewBlock:
        block = next((block for block in self.blocks if block.block_id == block_id), None)
        if block is None:
            raise Exception(f'Block with id {block_id} not found')
        return block

    def get_blocks(self) -> List[RichViewBlock]:
        return [block for block in self.blocks]

    def add_block(self, block: RichViewBlock) -> RichViewBlock:
        if not isinstance(block, RichViewBlock):
            raise Exception('Block must be a RichViewBlock')

        url_ending = f"report/{self.report_id}/block"
        body = block._asdict(assign_id=False)

        response = self.session._post(url_ending, body=body)
        if not response.ok:
            raise Exception(f'Failed to create block: {response.status_code} {response.text}')
        self.synced_with_server = False

        response_block = _convert_block(response.json()['result'],
                                        session=self.session,
                                        report_id=self.report_id)
        self.blocks.append(response_block)
        return response_block

    def delete_block(self, block_id: str) -> RichViewReport:
        new_blocks = [block for block in self.blocks if block.block_id != block_id]
        url_ending = f"report/{self.report_id}"
        body = {"content": {"blocks": [block._asdict() for block in new_blocks]}}
        response = self.session._put(url_ending, body=body)
        if not response.ok:
            raise Exception(f'Failed to delete block: {response.status_code} {response.text}')
        self.synced_with_server = False
        return RichViewReport(**response.json()['result'],
                              blocks=response.json()['result']['content']['blocks'],
                              session=self.session)

    def update_online_version(self) -> RichViewReport:
        url_ending = f"report/{self.report_id}"
        body = {
            "content": {
                "blocks": [block._asdict() for block in self.blocks]
            },
            "title": self.title,
            "lastEdited": self.lastEdited
        }
        response = self.session._put(url_ending, body=body)
        if not response.ok:
            raise Exception(f'Failed to update server: {response.status_code} {response.text}')
        self.synced_with_server = True
        return self

    def get_online_version(self) -> RichViewReport:
        url_ending = f"report/{self.report_id}"
        response = self.session._get(url_ending)
        if not response.ok:
            raise Exception(f'Failed to get online version: {response.status_code} {response.text}')
        self.synced_with_server = True
        self.__init__(**response.json()['result'],
                      blocks=response.json()['result']['content']['blocks'],
                      session=self.session)
        return self


def check_if_all_properties_exist(nested_dict, reference_dict):
    for key, value in nested_dict.items():
        assert key in reference_dict.keys(
        ), f'Property {key} is a new chart option, current properties are {reference_dict.keys()}. If you are sure what you are doing, use force=True'
        if isinstance(value, dict):
            check_if_all_properties_exist(value, reference_dict[key])