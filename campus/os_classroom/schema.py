"""Explicit bilingual lesson contracts; authored content only, never learner code."""

def B(es, en):
    if not isinstance(es, str) or not isinstance(en, str) or not es.strip() or not en.strip():
        raise ValueError('Both language editions are required')
    return {'es': es, 'en': en}

def concept(title, body, takeaway):
    return dict(title=title, body=body, takeaway=takeaway)

def step(title, expected, command=''):
    return dict(title=title, expected=expected, command=command)

def example(title, shell, command, expected, explanation):
    return dict(title=title, shell=shell, command=command, expected=expected, explanation=explanation)

def lab(environment, steps, evidence, success, recovery, symptom, hint):
    return dict(environment=environment, steps=steps, evidence=evidence, success=success,
                recovery=recovery, symptom=symptom, hint=hint)

def quiz(question, options, correct, explanation):
    if type(correct) is not int or not 0 <= correct < len(options):
        raise ValueError('Invalid answer key')
    return dict(question=question, options=options, correct=correct, explanation=explanation)

def lesson(id, title, question, outcome, concepts, diagram, example, lab, quiz, mistake, summary, refs, legacy):
    return dict(id=id, title=title, question=question, outcome=outcome, concepts=concepts,
                diagram=diagram, example=example, lab=lab, quiz=quiz, mistake=mistake,
                summary=summary, refs=refs, legacy=legacy)
