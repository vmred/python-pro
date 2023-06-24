import pytest

from lessons.lesson_3.app.flask_start import app


class TestFlaskViews:
    cases = [
        (
            '/customers',
            200,
            [
                ['Luís', 'São José dos Campos', 'SP'],
                ['Leonie', 'Stuttgart', None],
                ['François', 'Montréal', 'QC'],
                ['Bjørn', 'Oslo', None],
                ['František', 'Prague', None],
                ['Helena', 'Prague', None],
                ['Astrid', 'Vienne', None],
                ['Daan', 'Brussels', None],
                ['Kara', 'Copenhagen', None],
                ['Eduardo', 'São Paulo', 'SP'],
                ['Alexandre', 'São Paulo', 'SP'],
                ['Roberto', 'Rio de Janeiro', 'RJ'],
                ['Fernanda', 'Brasília', 'DF'],
                ['Mark', 'Edmonton', 'AB'],
                ['Jennifer', 'Vancouver', 'BC'],
                ['Frank', 'Mountain View', 'CA'],
                ['Jack', 'Redmond', 'WA'],
                ['Michelle', 'New York', 'NY'],
                ['Tim', 'Cupertino', 'CA'],
                ['Dan', 'Mountain View', 'CA'],
                ['Kathy', 'Reno', 'NV'],
                ['Heather', 'Orlando', 'FL'],
                ['John', 'Boston', 'MA'],
                ['Frank', 'Chicago', 'IL'],
                ['Victor', 'Madison', 'WI'],
                ['Richard', 'Fort Worth', 'TX'],
                ['Patrick', 'Tucson', 'AZ'],
                ['Julia', 'Salt Lake City', 'UT'],
                ['Robert', 'Toronto', 'ON'],
                ['Edward', 'Ottawa', 'ON'],
                ['Martha', 'Halifax', 'NS'],
                ['Aaron', 'Winnipeg', 'MB'],
                ['Ellie', 'Yellowknife', 'NT'],
                ['João', 'Lisbon', None],
                ['Madalena', 'Porto', None],
                ['Hannah', 'Berlin', None],
                ['Fynn', 'Frankfurt', None],
                ['Niklas', 'Berlin', None],
                ['Camille', 'Paris', None],
                ['Dominique', 'Paris', None],
                ['Marc', 'Lyon', None],
                ['Wyatt', 'Bordeaux', None],
                ['Isabelle', 'Dijon', None],
                ['Terhi', 'Helsinki', None],
                ['Ladislav', 'Budapest', None],
                ['Hugh', 'Dublin', 'Dublin'],
                ['Lucas', 'Rome', 'RM'],
                ['Johannes', 'Amsterdam', 'VV'],
                ['Stanisław', 'Warsaw', None],
                ['Enrique', 'Madrid', None],
                ['Joakim', 'Stockholm', None],
                ['Emma', 'London', None],
                ['Phil', 'London', None],
                ['Steve', 'Edinburgh ', None],
                ['Mark', 'Sidney', 'NSW'],
                ['Diego', 'Buenos Aires', None],
                ['Luis', 'Santiago', None],
                ['Manoj', 'Delhi', None],
                ['Puja', 'Bangalore', None],
            ],
        ),
        (
            '/customers?state=SP',
            200,
            [["Luís", "São José dos Campos", "SP"], ["Eduardo", "São Paulo", "SP"], ["Alexandre", "São Paulo", "SP"]],
        ),
        ('/customers?city=São Paulo', 200, [["Eduardo", "São Paulo", "SP"], ["Alexandre", "São Paulo", "SP"]]),
        ('/customers?city=São Paulo&state=SP', 200, [['Eduardo', 'São Paulo', 'SP'], ['Alexandre', 'São Paulo', 'SP']]),
        ('/customers?city=vcz', 200, []),
    ]

    @pytest.mark.homework4
    @pytest.mark.parametrize('query, status_code, expected', cases, ids=[x[0] for x in cases])
    def test_view_get_customers(self, query, status_code, expected):
        with app.test_client() as test_client:
            response = test_client.get(query)
            assert response.status_code == status_code
            assert response.json == expected
