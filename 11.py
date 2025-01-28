colleagues = ['Семён Семёнов', 'Ольга Петрова', 'Фёдор Фёдоров', 'Кирилл Кириллов', 'Анатолий Карпов']
positions = ['Стажёр-аналитик', 'Аналитик', 'Инженер данных', 'Аналитик-разработчик', 'Руководитель отдела аналитики']

colleagues_info = []
for colleague, position in zip(colleagues,positions):
    x={
        'colleague':colleague,
        'position':position
    }
    colleagues_info.append(x)
print(colleagues_info)

