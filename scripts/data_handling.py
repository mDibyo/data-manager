#!/usr/bin/env python3

from data import DataTableMappingTemplateGenerator


__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


mapping = {
    'student': 'Student',
    'reader': 'Reader',
    'time': 'Time',
    'problems': {
        'q1': {
            'a': {
                'grade': 'Problem 1.a',
                'comment': 'Problem 1.a Comment',
                },
            'b': {
                'grade': 'Problem 1.b',
                'comment': 'Problem 1.b Comment',
                },
            'c': {
                'grade': 'Problem 1.c',
                'comment': 'Problem 1.c Comment',
                },
            }
    }
}

StudentMapping = DataTableMappingTemplateGenerator('student', 'Student')
ReaderMapping = DataTableMappingTemplateGenerator('reader', 'Reader')
TimeMapping = DataTableMappingTemplateGenerator('time', 'Time')
CommentMapping = \
    DataTableMappingTemplateGenerator('comment',
                                      'Problem $problem.$grade Comment')
GradeMapping = \
    DataTableMappingTemplateGenerator('grade', 'Problem $problem.$grade')
PartMapping = DataTableMappingTemplateGenerator('$part')
ProblemMapping = DataTableMappingTemplateGenerator('$problem')
ProblemsMapping = DataTableMappingTemplateGenerator('problems')

HomeworkSelfGradesMapping = \
    DataTableMappingTemplateGenerator('hw$hwnumber_selfgrades',
                                      submappings=[StudentMapping(),
                                                   ReaderMapping(),
                                                   TimeMapping(),
                                                   ProblemsMapping()])
HomeworkReaderGradesMapping = \
    DataTableMappingTemplateGenerator('hw$hwnumber_readergrades',
                                      submappings=[StudentMapping(),
                                                   ReaderMapping(),
                                                   TimeMapping(),
                                                   ProblemsMapping()])