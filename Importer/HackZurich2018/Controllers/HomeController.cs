using HackZurich2018.AppOptions;
using HackZurich2018.Backend;
using HackZurich2018.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;

namespace HackZurich2018.Controllers
{
    public class HomeController : Controller
    {
        private Neo4jConnector _neo4j { get; set; }
        HttpClient client = new HttpClient();

        public HomeController(Neo4jConnector neo4j, IOptions<MainOptions> options)
        {
            _neo4j = neo4j;

            client.BaseAddress = new Uri("https://hack-docs.lex.tools/ch/cod/");
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", options.Value.LexToken);
        }

        public IActionResult Index()
        {
            return View();
        }

        private Func<ArticleImported, (Article Article, IEnumerable<Paragraph> Paragraphs)> SelectArticle(string CCNr)
        {
            return (ArticleImported a) =>
            {
                if ((a.type != "singleA" && a.type != "doubleA"))
                {
                    Debugger.Break();
                }
                try
                {
                    return (new Article
                    {
                        Id = a.id,
                        FullId = CCNr + a.id,
                        Marginalia = a.marginalia_text,
                        Numerical = a.numerical,
                        Title = a.title_text
                    }, a.paragraphs?.Select(p => new Paragraph
                    {
                        Numerical = p.numerical,
                        Text = p.text
                    }) ?? new List<Paragraph>());
                } catch (Exception e)
                {
                    Debugger.Break();
                    throw e;
                }
                
            };
        }

        public async Task<IActionResult> CrawlList()
        {
            var list = "101,122,124,141,142.2,142.31,142.512,151.1,152.1,152.11,152.3,152.31,161.1,161.116,170.512,171.1,171.13,171.14,172.01,172.021,172.061,172.081,172.222.1,173.41,191.11,192.12,192.121,192.126,195.1,195.11,196.1"
                .Split(',').ToList();

            foreach (var cod in list)
            {
                await CrawlCod(cod);
            }

            return new EmptyResult();
        }

        public async Task<IActionResult> CrawlCod(string cod)
        {
            var response = await client.GetAsync(cod);

            if (!response.IsSuccessStatusCode)
            {
                Debugger.Break();

            }
            try
            {
                var data = await response.Content.ReadAsAsync<ClassifiedCompilationFromService>();

                if (data?.compilation != "")
                {
                    Debugger.Break();
                }
                var cc = new ClassifiedCompilation()
                {
                    CCNr = cod,
                    Title = data.title.en,
                    OriginalUrl = data.original_url.en,
                    EffectiveDate = DateTime.Parse(data.effective_date),
                    EnactmentDate = DateTime.Parse(data.enactment_date),
                    Categories = data.categories.en,
                    //Compilation = data.compilation
                };

                var selectArticle = SelectArticle(cc.CCNr);

                var articles = data.content.en.articles.Select(selectArticle).ToList();
                var sections = new Queue<SectionImported>();
                sections.Enqueue(data.content.en);

                while (sections.Count > 0)
                {
                    var section = sections.Dequeue();

                    articles.AddRange(section.articles.Select(selectArticle));

                    section.children.ForEach(sections.Enqueue);
                }

                _neo4j.MergeCc(cc);

                _neo4j.MergeArticles(cc.CCNr, articles.Select(a => a.Article));

                _neo4j.MergeParagraphs(articles);
            }
            catch (Exception e)
            {
                Debugger.Break();
            }

            return new EmptyResult();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
