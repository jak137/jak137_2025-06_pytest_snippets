import pickle

import pytest

from sample_module.steps import build_model, predict_text


@pytest.mark.order(2)
def test_predict_with_model(tests_results_path):
    with open(tests_results_path / 'en_pl.pic', 'rb') as f:
        model = pickle.load(f)

    txt1 = '''The Parties agree that an armed attack against one or more of them in Europe or North America shall be 
    considered an attack against them all and consequently they agree that, if such an armed attack occurs, each of 
    them, in exercise of the right of individual or collective self-defence recognised by Article 51 of the Charter of 
    the United Nations, will assist the Party or Parties so attacked by taking forthwith, individually and in concert 
    with the other Parties, such action as it deems necessary, including the use of armed force, to restore and 
    maintain the security of the North Atlantic area.

    Any such armed attack and all measures taken as a result thereof shall immediately be reported to the Security 
    Council. Such measures shall be terminated when the Security Council has taken the measures necessary to restore 
    and maintain international peace and security .
    '''

    p_en, p_pl = predict_text(model, txt1)
    print('\n\n', p_en, p_pl)
    assert p_en > p_pl

    txt2 = '''Strony zgadzają się, że zbrojna napaść na jedną lub kilka z nich w Europie lub Ameryce Północnej będzie 
    uważana za napaść przeciwko nim wszystkim; wskutek tego zgadzają się one na to, że jeżeli taka zbrojna napaść 
    nastąpi, każda z nich, w wykonaniu prawa do indywidualnej lub zbiorowej samoobrony, uznanego przez Artykuł 51 Karty 
    Narodów Zjednoczonych, udzieli pomocy Stronie lub Stronom tak napadniętym, podejmując natychmiast indywidualnie i 
    w porozumieniu z innymi Stronami taką akcję, jaką uzna za konieczną, nie wyłączając użycia siły zbrojnej, w celu 
    przywrócenia i utrzymania bezpieczeństwa obszaru północnoatlantyckiego. 
    
    O każdej takiej zbrojnej napaści i o wszystkich środkach zastosowanych w jej wyniku zostanie bezzwłocznie 
    powiadomiona Rada Bezpieczeństwa. Środki takie zostaną zaniechane, gdy tylko Rada Bezpieczeństwa podejmie działania 
    konieczne do przywrócenia i utrzymania międzynarodowego pokoju i bezpieczeństwa.
    '''

    p_en, p_pl = predict_text(model, txt2)
    print('\n\n', p_en, p_pl)
    assert p_en < p_pl


@pytest.mark.order(1)
def test_build_model(sample_data_path, tests_results_path):
    with open(sample_data_path / 'ai_act_en.xhtml') as f1, open(sample_data_path / 'ai_act_pl.xhtml') as f2:
        model = build_model(f1, f2)
    with open(tests_results_path / 'en_pl.pic', 'wb') as f:
        pickle.dump(model, f)
