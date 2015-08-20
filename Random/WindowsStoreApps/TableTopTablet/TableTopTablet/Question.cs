using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TableTopTablet
{
    public class Question
    {
        public Question() { }

        public Question(string questionTitle)
        {
            QuestionTitle = questionTitle;
        }

        public string QuestionTitle { get; set; }

        public override string ToString()
        {
            return QuestionTitle;
        }
    }
}
