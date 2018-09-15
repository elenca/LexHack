using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace HackZurich2018.Models
{
    public class ClassifiedCompilation
    {
        public string Title { get; set; }
        public string CCNr { get; set; }
        public DateTime EnactmentDate { get; set; }
        public DateTime EffectiveDate { get; set; }
        //public string Compilation { get; set; }
        public string OriginalUrl { get; set; }
        public List<string> Categories { get; set; }
    }

    public class Article
    {
        public string Id { get; set; }
        public string FullId { get; set; }
        public string Title { get; set; }
        public string Marginalia { get; set; }
        public string Numerical { get; set; }
    }

    public class Paragraph
    {
        public string Text { get; set; }
        public string Numerical { get; set; }
    }
}
