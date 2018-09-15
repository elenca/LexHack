using System.Collections.Generic;

namespace HackZurich2018.Models
{
    public class Title
    {
        public string en { get; set; }
    }

    public class OriginalUrlImported
    {
        public string en { get; set; }
    }

    public class ParagraphImported
    {
        public string html { get; set; }
        public string numerical { get; set; }
        public string text { get; set; }
    }

    public class ArticleImported
    {
        public bool @double { get; set; }
        //public Fns fns { get; set; }
        public string id { get; set; }
        public string litera { get; set; }
        //public List<string> marginale { get; set; }
        //public string marginalia { get; set; }
        public string marginalia_text { get; set; }
        public string numerical { get; set; }
        public List<ParagraphImported> paragraphs { get; set; }
        public bool range { get; set; }
        //public string title { get; set; }
        public string title_text { get; set; }
        public string type { get; set; }
    }

    public class SectionImported
    {
        public List<ArticleImported> articles { get; set; }
        public List<SectionImported> children { get; set; }
        public string id { get; set; }
        public int level { get; set; }
        public string name_text { get; set; }
        public string title { get; set; }
        
        public string name { get; set; }
        public string praeambel { get; set; }
        public string praeambel_text { get; set; }
        public string subHeader { get; set; }
        public string subHeader_text { get; set; }
        public string subTitle { get; set; }
    }

    public class Content
    {
        public SectionImported en { get; set; }
    }

    public class Categories
    {
        public List<string> en { get; set; }
    }

    public class ClassifiedCompilationFromService
    {
        public Title title { get; set; }
        public string sr_number { get; set; }
        public string enactment_date { get; set; }
        public string effective_date { get; set; }
        public string compilation { get; set; }
        public OriginalUrlImported original_url { get; set; }
        public Content content { get; set; }
        public Categories categories { get; set; }
    }
}
