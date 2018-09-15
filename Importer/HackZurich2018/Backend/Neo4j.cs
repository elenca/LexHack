using HackZurich2018.AppOptions;
using HackZurich2018.Models;
using Microsoft.Extensions.Options;
using Neo4j.Driver.V1;
using Neo4jClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace HackZurich2018.Backend
{
    public class Neo4jConnector : IDisposable
    {
        private static readonly NLog.ILogger _log = NLog.LogManager.GetCurrentClassLogger();
        private readonly BoltGraphClient _neo4j;

        public Neo4jConnector(IOptions<Neo4jOptions> options)
        {
            var opt = options.Value;

            var driver = GraphDatabase.Driver(opt.Uri, AuthTokens.Basic(opt.User, opt.Password));
            _neo4j = new BoltGraphClient(driver);

            _neo4j.Connect();
            
        }

        public void Dispose()
        {
            _neo4j?.Dispose();
        }
        public void MergeCc(ClassifiedCompilation cc)
        {
             _neo4j.Cypher
                .WithParam("cc", cc)
                .Merge("(c:ClassifiedCompilation {CCNr: {cc}.CCNr})")
                .Set("c += {cc}")
                .ExecuteWithoutResults();
        }
        public void MergeArticles(string cCNr, IEnumerable<Article> articles)
        {
             _neo4j.Cypher
                .WithParam("ccnr", cCNr)
                .Match("(c:ClassifiedCompilation {CCNr: {ccnr}})")
                .Unwind(articles, "article")
                .Merge("(c)-[:HAS_ARTICLE]->(a:Article {FullId: article.FullId})")
                .Set("a += article")
                .ExecuteWithoutResults();

        }
        public void MergeParagraphs(IEnumerable<(Article Article, IEnumerable<Paragraph> Paragraphs)> a_Paragraphs)
        {
            var ll = new List<(string articleId, Paragraph Paragraph)>();
            foreach (var (Article, Paragraphs) in a_Paragraphs)
            {
                foreach (var item in Paragraphs)
                {
                    ll.Add((Article.FullId, item));
                }
            }

             _neo4j.Cypher
                .Unwind(ll.Select(l => new { l.articleId, l.Paragraph }), "para")
                .Match("(a:Article {FullId: para.articleId})")
                .Merge("(a)-[:HAS_PARAGRAPH]->(p:Paragraph {Numerical: para.Paragraph.Numerical})")
                .Set("p += para.Paragraph")
                .ExecuteWithoutResults();

        }
    }
}
