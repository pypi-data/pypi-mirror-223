import pandas as pd
import numpy as np
import time
from datetime import datetime

from SharedData.Logger import Logger


class SharedNumpy(np.ndarray):

    def __new__(cls, shape, dtype=None, buffer=None, offset=0, strides=None, order=None):
        obj = np.ndarray.__new__(
            cls, shape, dtype, buffer, offset, strides, order)
        obj.table = None
        return obj

    def subscribe(self,host,port):
        self.table.subscribe(host, port)

    def preallocate(self):
        # TODO: add a progress bar if memory to be preallocated too high
        arr = super().__getitem__(slice(0, self.size))
        arr['mtime'][:] = np.datetime64('NaT')
    ############################## KEYLESS OPERATIONS ########################################

    def insert(self, new_records):
        self.table.acquire()

        try:
            nrec = new_records.size
            _count = self.count
            if (_count + nrec <= self.size):
                # convert new_records
                if (self.dtype != new_records.dtype):
                    new_records = self.convert(new_records)
                # fill mtime
                nidx = np.isnat(new_records['mtime'])
                if nidx.any():
                    new_records['mtime'][nidx] = time.time_ns()

                arr = super().__getitem__(slice(0, self.size))
                arr[_count:_count+nrec] = new_records
                self.count = _count + nrec
                self.mtime = datetime.now().timestamp()
            else:
                Logger.log.error('Table max size reached!')
        except Exception as e:
            Logger.log.error('Error inserting records!\n%s' % (e))

        self.table.release()

    def overwrite(self, new_records):
        self.table.acquire()

        try:
            # assume new_records is sorted
            # overwrite based on the first date
            if isinstance(new_records, pd.DataFrame):
                new_records = self.table.df2records(new_records)
            elif (self.dtype != new_records.dtype):
                new_records = self.convert(new_records)
            # fill mtime
            nidx = np.isnat(new_records['mtime'])
            if nidx.any():
                new_records['mtime'][nidx] = time.time_ns()

            nrec = new_records.size
            _count = self.count
            # overwrite from first date
            fdate = new_records[0]['date']
            fdateid = np.where(self['date'] >= fdate)[0]
            if np.any(fdateid):
                _count = fdateid[0]
            # set data
            if (_count + nrec <= self.size):
                arr = super().__getitem__(slice(0, self.size))
                arr[_count:_count+nrec] = new_records
                self.count = _count + nrec
                self.minchgid = _count
                self.mtime = datetime.now().timestamp()
            else:
                Logger.log.error('Table max size reached!')
        except Exception as e:
            Logger.log.error('Error overwriting records!\n%s' % (e))

        self.table.release()

    ############################## PRIMARY KEY OPERATIONS ########################################
    def upsert(self, new_records):
        if new_records.size>0:
                        
            # convert to same dtype record
            if isinstance(new_records, pd.DataFrame):
                new_records = self.table.df2records(new_records)
            elif (self.dtype != new_records.dtype):
                new_records = self.convert(new_records)

            # fill mtime
            nidx = np.isnat(new_records['mtime'])
            if nidx.any():
                new_records['mtime'][nidx] = time.time_ns()

            # single record to array
            if new_records.shape == ():
                new_records = np.array([new_records])

            self.table.acquire()
            
            try:                
                # initialize pkey
                if not self.keys.initialized:
                    self.keys.initialize()
                # upsert
                minchgid = self.count
                arr = super().__getitem__(slice(0, self.size))
                if 'date_portfolio_' in self.table.keys.pkeystr:
                    self.count, minchgid = self.keys.upsert_func(
                        arr, self.count, new_records, self.pkey,\
                        self.keys.dateiniidx,self.keys.dateendidx,self.keys.dateunit,\
                        self.keys.portiniidx,self.keys.portendidx,self.keys.portlist,self.keys.portlistcount)
                    self.keys.portlistcount = self.count
                else:
                    self.count, minchgid = self.keys.upsert_func(
                        arr, self.count, new_records, self.pkey,\
                        self.keys.dateiniidx,self.keys.dateendidx,self.keys.dateunit)

                # table full
                if self.count == self.size:                    
                    Logger.log.error('Table %s/%s is full!' %
                        (self.table.source, self.table.tablename))
                    raise Exception('Table %s/%s is full!' %
                        (self.table.source, self.table.tablename))
                minchgid = int(minchgid)
                self.minchgid = minchgid
                self.mtime = datetime.now().timestamp()
            except Exception as e:
                Logger.log.error('Error upserting records!\n%s' % (e))

            self.table.release()
            return minchgid
        return self.count

    def get_loc(self, keys):
        self.table.acquire()

        try:
            # initialize pkey
            if not self.keys.initialized:
                self.keys.initialize()            
            loc = self.keys.get_loc_func(self[:], self.pkey, keys).astype(int)
            
        except Exception as e:
            Logger.log.error('Error getting loc!\n%s' % (e))
            loc = np.array([])

        self.table.release()
        return loc

    def sort_index(self, start=0):
        self.table.acquire()
        try:

            keys = tuple(self[column][start:]
                         for column in self.table.keys.pkeycolumns[::-1])
            idx = np.lexsort(keys)

            shift_idx = np.roll(idx, 1)
            if len(shift_idx) > 0:
                shift_idx[0] = -1
                idx_diff = idx - shift_idx
                unsortered_idx = np.where(idx_diff != 1)[0]
                if np.where(idx_diff != 1)[0].any():
                    _minchgid = np.min(unsortered_idx) + start
                    self.minchgid = _minchgid
                    self[start:] = self[start:][idx]
                    if not self.keys.initialized:
                        self.keys.initialize()
                    else:
                        self.keys.update_index(_minchgid)
        except Exception as e:
            Logger.log.error('Error sorting index!\n%s' % (e))

        self.table.release()

    def write(self):
        self.table.write()

    def records2df(self, records):
        return self.table.records2df(records)
    
    def df2records(self, df):
        return self.table.df2records(df)
    
    def convert(self, new_records):
        rec = np.full((new_records.size,), fill_value=np.nan, dtype=self.dtype)
        for col in self.dtype.names:
            if col in new_records.dtype.names:
                try:
                    rec[col] = new_records[col].astype(self.dtype[col])
                except:
                    Logger.log.error('Could not convert %s!' % (col))
        return rec

    def get_date_loc(self,date):
        if not self.keys.initialized:
            self.keys.initialize()
        dtint = int(date.value/24/60/60/10**9)
        dtiniid = self.keys.dateiniidx[dtint]
        dtendid = self.keys.dateendidx[dtint]        
        return [dtiniid,dtendid+1]
    
    def get_index_date_portfolio(self,keys):    
        if not self.keys.initialized:
            self.keys.initialize()    
        return self.keys.get_index_date_portfolio_func(self[:], keys, self.pkey, self.keys.portiniidx,self.keys.portlist)
            
    ############################## GETTERS / SETTERS ##############################

    def __getitem__(self, key):
        if hasattr(self, 'table'):
            arr = super().__getitem__(slice(0, self.count))  # slice arr
            if self.count > 0:                
                return arr.__getitem__(key)
            else:
                return arr
        else:
            return super().__getitem__(key)

    def free(self):
        self.table.free()

    @property
    def count(self):
        return self.table.hdr['count']

    @count.setter
    def count(self, value):
        self.table.hdr['count'] = value

    @property
    def mtime(self):
        return self.table.hdr['mtime']

    @mtime.setter
    def mtime(self, value):
        self.table.hdr['mtime'] = value

    @property
    def minchgid(self):
        return self.table.hdr['minchgid']

    @minchgid.setter
    def minchgid(self, value):
        value = min(value, self.table.hdr['minchgid'])
        self.table.hdr['minchgid'] = value

    @property
    def keys(self):
        return self.table.keys

    @keys.setter
    def keys(self, value):
        self.table.keys = value

    @property
    def pkey(self):
        return self.table.keys.pkey

    @pkey.setter
    def pkey(self, value):
        self.table.keys.pkey = value
