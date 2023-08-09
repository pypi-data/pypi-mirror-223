from typing import IO, Optional
from urllib.parse import urljoin
from uuid import uuid4

import pandas as pd
from progressbar import Bar, Percentage, ProgressBar
from requests import Session

from datarefiner_client.api.entities import Upload
from datarefiner_client.dataframe_uploader import DataFrameUploader
from datarefiner_client.exceptions import DatarefinerClientUploadError


class UploadsEntrypoints:
    _base_url: str
    session: Session

    def __init__(self, *args, **kwargs):
        self._uploads_url = urljoin(self._base_url, "/upload")
        super(UploadsEntrypoints, self).__init__(*args, **kwargs)

    def _upload(self, _io: IO, title: Optional[str] = None) -> Upload:
        """
        Upload IO to Datarefiner server
        :param _io: File or Reader
        :return: Information about uploaded file on datarefiner server
        """
        title = title or f"{uuid4()}.csv"
        with self.session.post(url=self._uploads_url, files={"file": (title, _io)}) as resp:
            if not resp.ok:
                raise DatarefinerClientUploadError(response=resp)
            return Upload(**resp.json()["upload"])

    def upload(self, df: pd.DataFrame, title: Optional[str] = None) -> Upload:
        pbar = ProgressBar(widgets=["Upload dataframe: ", Percentage(), Bar()])
        df_io = DataFrameUploader(df, cb=lambda size: pbar.update(pbar.currval + size))
        pbar.maxval = len(df_io)
        pbar.start()
        upload = self._upload(_io=df_io, title=title)
        pbar.finish()
        return upload
