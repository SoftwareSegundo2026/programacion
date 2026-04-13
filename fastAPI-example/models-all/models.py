from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'Artist'
    ArtistId = Column(Integer, primary_key=True)
    Name = Column(String(120))

class Album(Base):
    __tablename__ = 'Album'
    AlbumId = Column(Integer, primary_key=True)
    Title = Column(String(160), nullable=False)
    ArtistId = Column(Integer, ForeignKey('Artist.ArtistId'), nullable=False)
    artist = relationship('Artist', backref='albums')

class Employee(Base):
    __tablename__ = 'Employee'
    EmployeeId = Column(Integer, primary_key=True)
    LastName = Column(String(20), nullable=False)
    FirstName = Column(String(20), nullable=False)
    Title = Column(String(30))
    ReportsTo = Column(Integer, ForeignKey('Employee.EmployeeId'))
    BirthDate = Column(DateTime)
    HireDate = Column(DateTime)
    Address = Column(String(70))
    City = Column(String(40))
    State = Column(String(40))
    Country = Column(String(40))
    PostalCode = Column(String(10))
    Phone = Column(String(24))
    Fax = Column(String(24))
    Email = Column(String(60))
    manager = relationship('Employee', remote_side=[EmployeeId], backref='subordinates')

class Customer(Base):
    __tablename__ = 'Customer'
    CustomerId = Column(Integer, primary_key=True)
    FirstName = Column(String(40), nullable=False)
    LastName = Column(String(20), nullable=False)
    Company = Column(String(80))
    Address = Column(String(70))
    City = Column(String(40))
    State = Column(String(40))
    Country = Column(String(40))
    PostalCode = Column(String(10))
    Phone = Column(String(24))
    Fax = Column(String(24))
    Email = Column(String(60), nullable=False)
    SupportRepId = Column(Integer, ForeignKey('Employee.EmployeeId'))
    support_rep = relationship('Employee', backref='customers')

class Genre(Base):
    __tablename__ = 'Genre'
    GenreId = Column(Integer, primary_key=True)
    Name = Column(String(120))

class MediaType(Base):
    __tablename__ = 'MediaType'
    MediaTypeId = Column(Integer, primary_key=True)
    Name = Column(String(120))

class Track(Base):
    __tablename__ = 'Track'
    TrackId = Column(Integer, primary_key=True)
    Name = Column(String(200), nullable=False)
    AlbumId = Column(Integer, ForeignKey('Album.AlbumId'))
    MediaTypeId = Column(Integer, ForeignKey('MediaType.MediaTypeId'), nullable=False)
    GenreId = Column(Integer, ForeignKey('Genre.GenreId'))
    Composer = Column(String(220))
    Milliseconds = Column(Integer, nullable=False)
    Bytes = Column(Integer)
    UnitPrice = Column(Numeric(10, 2), nullable=False)
    album = relationship('Album', backref='tracks')
    media_type = relationship('MediaType', backref='tracks')
    genre = relationship('Genre', backref='tracks')

class Invoice(Base):
    __tablename__ = 'Invoice'
    InvoiceId = Column(Integer, primary_key=True)
    CustomerId = Column(Integer, ForeignKey('Customer.CustomerId'), nullable=False)
    InvoiceDate = Column(DateTime, nullable=False)
    BillingAddress = Column(String(70))
    BillingCity = Column(String(40))
    BillingState = Column(String(40))
    BillingCountry = Column(String(40))
    BillingPostalCode = Column(String(10))
    Total = Column(Numeric(10, 2), nullable=False)
    customer = relationship('Customer', backref='invoices')

class InvoiceLine(Base):
    __tablename__ = 'InvoiceLine'
    InvoiceLineId = Column(Integer, primary_key=True)
    InvoiceId = Column(Integer, ForeignKey('Invoice.InvoiceId'), nullable=False)
    TrackId = Column(Integer, ForeignKey('Track.TrackId'), nullable=False)
    UnitPrice = Column(Numeric(10, 2), nullable=False)
    Quantity = Column(Integer, nullable=False)
    invoice = relationship('Invoice', backref='invoice_lines')
    track = relationship('Track', backref='invoice_lines')

class Playlist(Base):
    __tablename__ = 'Playlist'
    PlaylistId = Column(Integer, primary_key=True)
    Name = Column(String(120))

class PlaylistTrack(Base):
    __tablename__ = 'PlaylistTrack'
    PlaylistId = Column(Integer, ForeignKey('Playlist.PlaylistId'), primary_key=True)
    TrackId = Column(Integer, ForeignKey('Track.TrackId'), primary_key=True)
    playlist = relationship('Playlist', backref='playlist_tracks')
    track = relationship('Track', backref='playlist_tracks')