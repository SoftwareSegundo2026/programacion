from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Artist(db.Model):
    __tablename__ = 'Artist'
    ArtistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))

class Album(db.Model):
    __tablename__ = 'Album'
    AlbumId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(160), nullable=False)
    ArtistId = db.Column(db.Integer, db.ForeignKey('Artist.ArtistId'), nullable=False)
    artist = db.relationship('Artist', backref='albums')

class Employee(db.Model):
    __tablename__ = 'Employee'
    EmployeeId = db.Column(db.Integer, primary_key=True)
    LastName = db.Column(db.String(20), nullable=False)
    FirstName = db.Column(db.String(20), nullable=False)
    Title = db.Column(db.String(30))
    ReportsTo = db.Column(db.Integer, db.ForeignKey('Employee.EmployeeId'))
    BirthDate = db.Column(db.DateTime)
    HireDate = db.Column(db.DateTime)
    Address = db.Column(db.String(70))
    City = db.Column(db.String(40))
    State = db.Column(db.String(40))
    Country = db.Column(db.String(40))
    PostalCode = db.Column(db.String(10))
    Phone = db.Column(db.String(24))
    Fax = db.Column(db.String(24))
    Email = db.Column(db.String(60))
    manager = db.relationship('Employee', remote_side=[EmployeeId], backref='subordinates')

class Customer(db.Model):
    __tablename__ = 'Customer'
    CustomerId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(40), nullable=False)
    LastName = db.Column(db.String(20), nullable=False)
    Company = db.Column(db.String(80))
    Address = db.Column(db.String(70))
    City = db.Column(db.String(40))
    State = db.Column(db.String(40))
    Country = db.Column(db.String(40))
    PostalCode = db.Column(db.String(10))
    Phone = db.Column(db.String(24))
    Fax = db.Column(db.String(24))
    Email = db.Column(db.String(60), nullable=False)
    SupportRepId = db.Column(db.Integer, db.ForeignKey('Employee.EmployeeId'))
    support_rep = db.relationship('Employee', backref='customers')

class Genre(db.Model):
    __tablename__ = 'Genre'
    GenreId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))

class MediaType(db.Model):
    __tablename__ = 'MediaType'
    MediaTypeId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))

class Track(db.Model):
    __tablename__ = 'Track'
    TrackId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    AlbumId = db.Column(db.Integer, db.ForeignKey('Album.AlbumId'))
    MediaTypeId = db.Column(db.Integer, db.ForeignKey('MediaType.MediaTypeId'), nullable=False)
    GenreId = db.Column(db.Integer, db.ForeignKey('Genre.GenreId'))
    Composer = db.Column(db.String(220))
    Milliseconds = db.Column(db.Integer, nullable=False)
    Bytes = db.Column(db.Integer)
    UnitPrice = db.Column(db.Numeric(10, 2), nullable=False)
    album = db.relationship('Album', backref='tracks')
    media_type = db.relationship('MediaType', backref='tracks')
    genre = db.relationship('Genre', backref='tracks')

class Invoice(db.Model):
    __tablename__ = 'Invoice'
    InvoiceId = db.Column(db.Integer, primary_key=True)
    CustomerId = db.Column(db.Integer, db.ForeignKey('Customer.CustomerId'), nullable=False)
    InvoiceDate = db.Column(db.DateTime, nullable=False)
    BillingAddress = db.Column(db.String(70))
    BillingCity = db.Column(db.String(40))
    BillingState = db.Column(db.String(40))
    BillingCountry = db.Column(db.String(40))
    BillingPostalCode = db.Column(db.String(10))
    Total = db.Column(db.Numeric(10, 2), nullable=False)
    customer = db.relationship('Customer', backref='invoices')

class InvoiceLine(db.Model):
    __tablename__ = 'InvoiceLine'
    InvoiceLineId = db.Column(db.Integer, primary_key=True)
    InvoiceId = db.Column(db.Integer, db.ForeignKey('Invoice.InvoiceId'), nullable=False)
    TrackId = db.Column(db.Integer, db.ForeignKey('Track.TrackId'), nullable=False)
    UnitPrice = db.Column(db.Numeric(10, 2), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    invoice = db.relationship('Invoice', backref='invoice_lines')
    track = db.relationship('Track', backref='invoice_lines')

class Playlist(db.Model):
    __tablename__ = 'Playlist'
    PlaylistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))

class PlaylistTrack(db.Model):
    __tablename__ = 'PlaylistTrack'
    PlaylistId = db.Column(db.Integer, db.ForeignKey('Playlist.PlaylistId'), primary_key=True)
    TrackId = db.Column(db.Integer, db.ForeignKey('Track.TrackId'), primary_key=True)
    playlist = db.relationship('Playlist', backref='playlist_tracks')
    track = db.relationship('Track', backref='playlist_tracks')