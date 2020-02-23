import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import CheckConstraint

Base = declarative_base()


class User(Base):
    __tablename__ = 'app_user'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    username = sa.Column(sa.String, unique=True)
    password = sa.Column(sa.String)
    nama = sa.Column(sa.String)
    jabatan = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True)

    def __init__(self, username, password, nama, jabatan, email):
        self.username = username
        self.password = password
        self.nama = nama
        self.jabatan = jabatan
        self.email = email


class Pasien(Base):
    __tablename__ = 'pasien'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    nama = sa.Column(sa.String, index=True)
    noKTP = sa.Column(sa.String, unique=True, index=True)
    notelp = sa.Column(sa.String,index=True)
    tglLahir = sa.Column(sa.Date)
    jenisKelamin = sa.Column(sa.String)
    alamat = sa.Column(sa.String, index=True)

    def __init__(self, nama, noKTP, notelp,tanggalLahir, jenisKelamin, alamat):
        self.nama = nama
        self.noKTP = noKTP
        self.notelp = notelp
        self.tglLahir = tanggalLahir
        self.jenisKelamin = jenisKelamin
        self.alamat = alamat

class CheckIn(Base):
    __tablename__ = 'check_in'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    PasienID = sa.Column(sa.String, sa.ForeignKey('pasien.noKTP'), index=True)
    Statusregistrasi = sa.Column(sa.String)
    metodebayar = sa.Column(sa.String)
    statusbayar = sa.Column(sa.String)
    waktuMulai = sa.Column(sa.DateTime)
    waktuSelesai = sa.Column(sa.DateTime)

    def __init__(self, PasienID, Statusregistrasi, metodebayar, statusbayar, waktuMulai=None,waktuSelesai=None):
        self.PasienID = PasienID
        self.Statusregistrasi = Statusregistrasi
        self.metodebayar = metodebayar
        self.statusbayar = statusbayar
        self.waktuMulai = waktuMulai
        self.waktuSelesai =waktuSelesai


class Lab(Base):
    __tablename__ = 'lab'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    nama = sa.Column(sa.String, index=True)
    kepalaLab = sa.Column(sa.String)
    alatTes = sa.Column(sa.String)


class Alat(Base):
    __tablename__ = 'alat'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    lab_id = sa.Column(sa.Integer, sa.ForeignKey('lab.id'), index=True)
    nama = sa.Column(sa.String,unique=True, index=True)
    harga = sa.Column(sa.Float)

class Perawat(Base):
    __tablename__ = 'perawat'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    lab_id = sa.Column(sa.Integer, sa.ForeignKey('lab.id'), index=True)
    nama = sa.Column(sa.String, index=True)
    statusPegawai = sa.Column(sa.String)
    notelp = sa.Column(sa.Integer)
    alamat = sa.Column(sa.String)


class Dokter(Base):
    __tablename__ = 'dokter'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    dokter_id = sa.Column(sa.String, unique=True, index=True)
    nama =sa.Column(sa.String,index=True)
    statusPegawai = sa.Column(sa.String)
    notelp = sa.Column(sa.Integer, index=True)
    alamat = sa.Column(sa.String)
    spesialis = sa.Column(sa.String)


class DokterLab(Base):
    __tablename__ = 'dokterLab'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    teslabID = sa.Column(sa.Integer, sa.ForeignKey('tesLab.id'))
    dokterID = sa.Column(sa.String, sa.ForeignKey('dokter.dokter_id'))


class TesLab(Base):
    __tablename__ = 'tesLab'
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    CheckInID = sa.Column(sa.Integer, sa.ForeignKey('check_in.id'), index=True)
    PerawatID = sa.Column(sa.Integer, sa.ForeignKey('perawat.id'))
    alatID = sa.Column(sa.String, sa.ForeignKey('alat.nama'))
    dokterPJ = sa.Column(sa.String, sa.ForeignKey('dokter.dokter_id'))
    noUrut = sa.Column(sa.Integer, autoincrement=True)
    statusVerif = sa.Column(sa.String)
    hasil = sa.Column(sa.TEXT)
    waktuMulai = sa.Column(sa.DateTime)
    waktuSelesai = sa.Column(sa.DateTime)

    def __init__(self, CheckInID, PerawatID, alatID, dokterPJ=None, statusVerif=None,hasil=None, waktuMulai=None,waktuSelesai=None):
        self.CheckInID = CheckInID
        self.PerawatID = PerawatID
        self.alatID = alatID
        self.dokterPJ = dokterPJ
        self.statusVerif=statusVerif
        self.hasil=hasil
        self.waktuMulai = waktuMulai
        self.waktuSelesai =waktuSelesai