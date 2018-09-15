#! /usr/bin/env python

from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

#
# class ClassifiedCompilation
#

class ClassifiedCompilation(GraphObject):
    __primarykey__ = "CCNr"

    Title = Property()
    CCNr = Property()
    EnactmentDate = Property()
    EffectiveDate = Property()
    Compilation = Property()
    OriginalUrl = Property()
    Categories = Property()

    articles = RelatedTo("Article", "HAS_ARTICLE")

    def __repr__(self):
        return "ClassifiedCompilation[CCNr={}, Title={}]".format(self.CCNr, self.Title)

    def toDict(self):
        return {
            "Title": self.Title,
            "CCNr": self.CCNr,
            "EnactmentDate": self.EnactmentDate,
            "EffectiveDate": self.EffectiveDate,
            "Compilation": self.Compilation,
            "OriginalUrl": self.OriginalUrl,
            "Categories": self.Categories,
            "articles": [a.toDict() for a in self.articles] }


#
# class Article
#

class Article(GraphObject):
    __primarykey__ = "FullId"

    Id = Property()
    FullId = Property()
    Title = Property()
    Marginalia = Property()
    Numerical = Property()

    paragraphs = RelatedTo("Paragraph", "HAS_PARAGRAPH")
    ClassifiedCompilation = RelatedFrom(ClassifiedCompilation, "HAS_ARTICLE")

    def __repr__(self):
        return "Article[Id={}, FullId={}, Title={}]".format(self.Id, self.FullId, self.Title)

    def toDict(self):
        return {
            "Id": self.Id,
            "FullId": self.FullId,
            "Title": self.Title,
            "Marginalia": self.Marginalia,
            "Numerical": self.Numerical,
            "Paragraphs": [p.toDict() for p in self.paragraphs],
            "ClassifiedCompilation": [c.CCNr for c in self.ClassifiedCompilation]}
#
# class Paragraph
#

class Paragraph(GraphObject):
    __primarykey__ = "Numerical"

    Text = Property()
    Numerical = Property()

    Article = RelatedFrom(Article, "HAS_ARTICLE")

    def __repr__(self):
        return "Paragraph[Text={}, Numerical={}]".format(self.Text, self.Numerical)

    def toDict(self):
        return {
            "Text": self.Text,
            "Numerical": self.Numerical
        }


#
# class Person
#

class Person(GraphObject):
    __primarykey__ = "Name"

    Name = Property()
    Position = Property()
    Company = RelatedFrom("Company", "EMPLOYS")
    Mails_sent = RelatedTo("Mail", "MAIL_FROM")
    Mails_received = RelatedFrom("Mail", "MAIL_TO")
    Accuser = RelatedTo("Case", "ACCUSER")
    Accused = RelatedFrom("Case", "ACCUSED")


    def __repr__(self):
        return "Person[Name={}, Position={}]".format(self.Name, self.Position)

    def toDict(self):
        return {
            "Name": self.Name,
            "Position": self.Position,
            "Company": [c.Name for c in self.Company],
            "Mails_sent": [m.toDict() for m in self.Mails_sent],
            "Mails_received": [m.toDict() for m in self.Mails_received],
            "Accuser": [a.toDict() for a in self.Accuser],
            "Accused": [a.toDict() for a in self.Accused]
        }


#
# class Company
#

class Company(GraphObject):
    __primarykey__ = "Name"

    Name = Property()
    persons = RelatedTo("Person", "EMPLOYS")

#
# class Mail
#

class Mail(GraphObject):
    __primarykey__ = "Subject"

    Subject = Property()
    Text = Property()
    Sender = RelatedFrom("Person", "MAIL_FROM")
    Receiver = RelatedTo("Person", "MAIL_TO")

    def toDict(self):
        return {
            "Subject": self.Subject,
            "Text": self.Text,
            "Sender": [s.Name for s in self.Sender],
            "Receiver": [r.Name for r in self.Receiver]
        }


#
# class Case
#

class Case(GraphObject):
    __primarykey__ = "Name"

    Name = Property()

    Related_to_mails = RelatedFrom("Mail", "RELATED_TO")
    Accuser = RelatedFrom("Person", "ACCUSER")
    Lawyer = RelatedFrom("Person", "WORKING_ON")

    def toDict(self):
        return {
            "Name": self.Name,
            "Related_to_Mails": [m.toDict() for m in self.Related_to_mails],
            "Accuser": [p.Name for p in self.Accuser][0],
            "Lawyer": [p.Name for p in self.Lawyer]
        }