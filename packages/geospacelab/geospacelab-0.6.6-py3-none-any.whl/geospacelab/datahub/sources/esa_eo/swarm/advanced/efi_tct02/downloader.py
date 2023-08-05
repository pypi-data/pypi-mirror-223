# Licensed under the BSD 3-Clause License
# Copyright (C) 2021 GeospaceLab (geospacelab)
# Author: Lei Cai, Space Physics and Astronomy, University of Oulu

__author__ = "Lei Cai"
__copyright__ = "Copyright 2021, GeospaceLab"
__license__ = "BSD-3-Clause License"
__email__ = "lei.cai@oulu.fi"
__docformat__ = "reStructureText"

from geospacelab import preferences as prf

from geospacelab.datahub.sources.esa_eo.swarm.downloader import Downloader as DownloaderModel


class Downloader(DownloaderModel):

    def __init__(
            self, dt_fr, dt_to,
            sat_id=None,
            data_type='TCT02',
            file_version=None,
            data_file_root_dir=None,
            ftp_data_dir=None,
            force=True, direct_download=True, **kwargs
    ):

        self.sat_id = sat_id

        if data_type == 'TCT02':
            frq_str = '2Hz'
        elif data_type == 'TCT16':
            frq_str = '16Hz'
        else:
            raise NotImplementedError

        if ftp_data_dir is None:
            ftp_data_dir = f'Advanced/Plasma_Data/{frq_str}_TII_Cross-track_Dataset/Sat_{sat_id.upper()}'

        if data_file_root_dir is None:
            data_file_root_dir = prf.datahub_data_root_dir / "ESA" / "SWARM" / "Advanced" / "EFI-TII" / data_type

        super(Downloader, self).__init__(
            dt_fr, dt_to,
            data_file_root_dir=data_file_root_dir,
            ftp_data_dir=ftp_data_dir,
            file_version=file_version,
            force=force, direct_download=direct_download, **kwargs
        )

    def download(self, **kwargs):

        done = super(Downloader, self).download(**kwargs)
        return done

    def search_files(self, **kwargs):

        file_list, versions = super(Downloader, self).search_files(**kwargs)

        return file_list, versions
        # version control