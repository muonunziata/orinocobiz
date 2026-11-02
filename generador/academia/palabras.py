"""Palabras de los widgets de la Academia en el tono del portal (usted), con su traducción de trabajo.

(es, fr, en, it, zh-tw). academia_web.py pone el español en los controles «Textos» de cada widget; build.py lo traduce
con traducciones.json, donde se copiaron estas traducciones (python3 -m academia.palabras las vuelve a copiar si faltan).
"""
WORDS = {
    'aula': {
        'lesson': ('Lección', 'Leçon', 'Lesson', 'Lezione', '課程單元'),
        'of': ('de', 'sur', 'of', 'di', '／'),
        'done': ('Marcar como estudiada', 'Marquer comme étudiée', 'Mark as studied', 'Segna come studiata', '標記為已學習'),
        'isdone': ('Estudiada', 'Étudiée', 'Studied', 'Studiata', '已學習'),
        'prev': ('Anterior', 'Précédente', 'Previous', 'Precedente', '上一個'),
        'next': ('Siguiente', 'Suivante', 'Next', 'Successiva', '下一個'),
        'soon': ('El video de esta lección está en preparación. Mientras tanto, aquí tiene el contenido completo.',
                 'La vidéo de cette leçon est en préparation. En attendant, voici le contenu complet.',
                 'The video for this lesson is being prepared. In the meantime, here is the full content.',
                 'Il video di questa lezione è in preparazione. Nel frattempo, ecco il contenuto completo.',
                 '本單元影片製作中。在此期間，請參閱完整內容。'),
        'summary': ('Contenido de la lección', 'Contenu de la leçon', 'Lesson content', 'Contenuto della lezione', '單元內容'),
        'practice': ('Práctica aplicada', 'Exercice appliqué', 'Applied practice', 'Esercitazione pratica', '應用練習'),
        'notes': ('Mis notas', 'Mes notes', 'My notes', 'I miei appunti', '我的筆記'),
        'notesph': ('Escriba aquí lo que quiera recordar. Se guarda en este dispositivo.', 'Écrivez ici ce que vous voulez retenir. C’est enregistré sur cet appareil.',
                    'Write here what you want to remember. It is saved on this device.', 'Scriva qui ciò che vuole ricordare. Si salva su questo dispositivo.',
                    '在此寫下您想記住的內容。內容會儲存在此裝置上。'),
        'res': ('Material', 'Ressource', 'Material', 'Materiale', '教材'),
        'list': ('Lecciones del curso', 'Leçons du cours', 'Course lessons', 'Lezioni del corso', '課程單元列表'),
        'quiz': ('Ir a la evaluación', 'Aller à l’évaluation', 'Go to the assessment', 'Vai alla valutazione', '前往評量'),
        'finish': ('Ha estudiado todas las lecciones. Ya puede presentar la evaluación final.', 'Vous avez étudié toutes les leçons. Vous pouvez passer l’évaluation finale.',
                   'You have studied every lesson. You can now take the final assessment.', 'Ha studiato tutte le lezioni. Ora può sostenere la valutazione finale.',
                   '您已學完所有單元，現在可以參加期末評量。'),
        'play': ('Reproducir', 'Lire', 'Play', 'Riproduci', '播放'),
        'consent': ('El video se carga desde', 'La vidéo est chargée depuis', 'The video loads from', 'Il video viene caricato da', '影片來源：'),
        'login': ('Su progreso se guarda en este dispositivo. Inicie sesión para conservarlo en su cuenta.',
                  'Votre progression est enregistrée sur cet appareil. Connectez-vous pour la conserver dans votre compte.',
                  'Your progress is saved on this device. Sign in to keep it in your account.',
                  'Il suo progresso si salva su questo dispositivo. Acceda per conservarlo nel suo account.',
                  '您的進度儲存在此裝置上。請登入以保存到您的帳戶。'),
    },
    'cabecera': {
        'start': ('Empezar el curso', 'Commencer le cours', 'Start the course', 'Inizia il corso', '開始課程'),
        'continue': ('Continuar', 'Continuer', 'Continue', 'Continua', '繼續'),
        'review': ('Repasar el curso', 'Revoir le cours', 'Review the course', 'Ripassa il corso', '複習課程'),
        'lessons': ('lecciones', 'leçons', 'lessons', 'lezioni', '個單元'),
        'quiz': ('evaluación final', 'évaluation finale', 'final assessment', 'valutazione finale', '期末評量'),
        'by': ('Imparte', 'Proposé par', 'By', 'A cura di', '授課：'),
        'badge': ('Insignia al aprobar:', 'Badge à la réussite :', 'Badge when you pass:', 'Distintivo al superamento:', '通過後獲得徽章：'),
        'progress': ('Su progreso', 'Votre progression', 'Your progress', 'Il suo progresso', '您的進度'),
        'trailer': ('Ver presentación', 'Voir la présentation', 'Watch the introduction', 'Guarda la presentazione', '觀看介紹'),
        'guide': ('Guía del curso (PDF)', 'Guide du cours (PDF)', 'Course guide (PDF)', 'Guida del corso (PDF)', '課程指南（PDF）'),
        'guide_t': ('Guía del curso', 'Guide du cours', 'Course guide', 'Guida del corso', '課程指南'),
        'contents': ('Contenido', 'Sommaire', 'Contents', 'Indice', '目錄'),
        'hours': ('Duración', 'Durée', 'Length', 'Durata', '時數'),
        'level': ('Nivel', 'Niveau', 'Level', 'Livello', '程度'),
        'guide_q': ('Haga la evaluación final en línea para recibir su certificado con código de verificación:',
                    'Passez l’évaluation finale en ligne pour recevoir votre certificat avec code de vérification :',
                    'Take the final assessment online to receive your certificate with a verification code:',
                    'Sostenga la valutazione finale online per ricevere il certificato con codice di verifica:',
                    '請於線上完成期末評量，以取得附驗證碼的證書：'),
        'page': ('Página %1$d de %2$d', 'Page %1$d sur %2$d', 'Page %1$d of %2$d', 'Pagina %1$d di %2$d', '第 %1$d 頁，共 %2$d 頁'),
    },
    'catalogo': {
        'search': ('Busque un curso…', 'Rechercher un cours…', 'Search for a course…', 'Cerchi un corso…', '搜尋課程…'),
        'all': ('Todas las escuelas', 'Toutes les écoles', 'All schools', 'Tutte le scuole', '所有學院'),
        'levels': ('Todos los niveles', 'Tous les niveaux', 'All levels', 'Tutti i livelli', '所有程度'),
        'lessons': ('lecciones', 'leçons', 'lessons', 'lezioni', '個單元'),
        'start': ('Ver curso', 'Voir le cours', 'See course', 'Vedi il corso', '查看課程'),
        'going': ('Continuar', 'Continuer', 'Continue', 'Continua', '繼續'),
        'done': ('Completado', 'Terminé', 'Completed', 'Completato', '已完成'),
        'none': ('No hay cursos con ese filtro.', 'Aucun cours ne correspond à ce filtre.', 'No courses match that filter.', 'Nessun corso con questo filtro.', '沒有符合此篩選條件的課程。'),
        'badge': ('Insignia', 'Badge', 'Badge', 'Distintivo', '徽章'),
        'soon': ('Videos en preparación', 'Vidéos en préparation', 'Videos coming soon', 'Video in preparazione', '影片製作中'),
    },
    'certificado': {
        'head': ('Certificado de aprobación', 'Certificat de réussite', 'Certificate of completion', 'Attestato di superamento', '結業證書'),
        'grants': ('certifica que', 'certifie que', 'certifies that', 'certifica che', '茲證明'),
        'passed': ('aprobó el curso', 'a réussi le cours', 'has passed the course', 'ha superato il corso', '已通過課程'),
        'on': ('el', 'le', 'on', 'il', '日期：'),
        'hours': ('Duración', 'Durée', 'Length', 'Durata', '時數'),
        'score': ('Calificación', 'Note', 'Score', 'Punteggio', '成績'),
        'code': ('Código de verificación', 'Code de vérification', 'Verification code', 'Codice di verifica', '驗證碼'),
        'print': ('Imprimir o guardar en PDF', 'Imprimer ou enregistrer en PDF', 'Print or save as PDF', 'Stampa o salva in PDF', '列印或儲存為 PDF'),
        'login': ('Inicie sesión para ver sus certificados.', 'Connectez-vous pour voir vos certificats.', 'Sign in to see your certificates.', 'Acceda per vedere i suoi certificati.', '請登入以查看您的證書。'),
        'notyet': ('Aún no tiene el certificado de este curso: apruebe la evaluación final.', 'Vous n’avez pas encore le certificat de ce cours : réussissez l’évaluation finale.',
                   'You do not have this course’s certificate yet: pass the final assessment.', 'Non ha ancora il certificato di questo corso: superi la valutazione finale.',
                   '您尚未取得本課程的證書：請先通過期末評量。'),
        'pick': ('Elija un curso desde «Mi aprendizaje».', 'Choisissez un cours dans « Mon apprentissage ».', 'Choose a course from “My learning”.', 'Scelga un corso da «Il mio apprendimento».', '請從「我的學習」選擇課程。'),
        'valid': ('Certificado válido', 'Certificat valide', 'Valid certificate', 'Certificato valido', '證書有效'),
        'invalid': ('No encontramos ningún certificado con ese código.', 'Aucun certificat ne correspond à ce code.', 'We could not find a certificate with that code.',
                    'Non troviamo nessun certificato con questo codice.', '查無此驗證碼的證書。'),
        'check': ('Comprobar un código', 'Vérifier un code', 'Check a code', 'Verifica un codice', '查驗驗證碼'),
    },
    'evaluacion': {
        'start': ('Empezar la evaluación', 'Commencer l’évaluation', 'Start the assessment', 'Inizia la valutazione', '開始評量'),
        'q': ('Pregunta', 'Question', 'Question', 'Domanda', '問題'),
        'of': ('de', 'sur', 'of', 'di', '／'),
        'check': ('Comprobar', 'Vérifier', 'Check', 'Verifica', '確認'),
        'next': ('Siguiente', 'Suivante', 'Next', 'Avanti', '下一題'),
        'results': ('Ver mi resultado', 'Voir mon résultat', 'See my result', 'Vedi il mio risultato', '查看結果'),
        'ok': ('Correcto', 'Correct', 'Correct', 'Corretto', '正確'),
        'ko': ('No es correcto', 'Ce n’est pas correct', 'Not correct', 'Non è corretto', '不正確'),
        'saved': ('Gracias, su respuesta quedó guardada.', 'Merci, votre réponse a été enregistrée.', 'Thank you, your answer has been saved.', 'Grazie, la sua risposta è stata salvata.', '謝謝，您的回答已儲存。'),
        'one': ('Elija una respuesta', 'Choisissez une réponse', 'Choose one answer', 'Scelga una risposta', '請選擇一個答案'),
        'many': ('Elija todas las que sean correctas', 'Choisissez toutes les bonnes réponses', 'Choose all that are correct', 'Scelga tutte quelle corrette', '請選擇所有正確答案'),
        'true': ('Verdadero', 'Vrai', 'True', 'Vero', '對'),
        'false': ('Falso', 'Faux', 'False', 'Falso', '錯'),
        'order': ('Arrastre para ordenar (o use las flechas)', 'Faites glisser pour ordonner (ou utilisez les flèches)', 'Drag to reorder (or use the arrows)',
                  'Trascini per ordinare (o usi le frecce)', '拖曳排序（或使用箭頭）'),
        'match': ('Relacione cada elemento con su pareja', 'Associez chaque élément à son correspondant', 'Match each item with its pair', 'Abbini ogni elemento alla sua coppia', '請將每一項配對'),
        'pick': ('Elija…', 'Choisir…', 'Choose…', 'Scelga…', '請選擇…'),
        'scale': ('Mueva el control: no hay respuestas buenas ni malas', 'Déplacez le curseur : il n’y a pas de bonne ou de mauvaise réponse',
                  'Move the slider: there are no right or wrong answers', 'Sposti il cursore: non ci sono risposte giuste o sbagliate', '移動滑桿：沒有對錯之分'),
        'reflect': ('Responda con sus palabras (no suma puntos)', 'Répondez avec vos mots (non noté)', 'Answer in your own words (not scored)',
                    'Risponda con parole sue (non conta per il punteggio)', '請用自己的話回答（不計分）'),
        'hint': ('Ver una pista', 'Voir un indice', 'Show a hint', 'Vedi un suggerimento', '查看提示'),
        'score': ('Su resultado', 'Votre résultat', 'Your result', 'Il suo risultato', '您的成績'),
        'need': ('Para aprobar se necesita', 'Pour réussir, il faut', 'To pass you need', 'Per superarla serve', '及格需達'),
        'pass': ('Aprobado. ¡Felicitaciones!', 'Réussi. Félicitations !', 'Passed. Congratulations!', 'Superata. Complimenti!', '通過，恭喜您！'),
        'fail': ('Todavía no. Repase las lecciones y vuelva a intentarlo.', 'Pas encore. Revoyez les leçons et réessayez.', 'Not yet. Review the lessons and try again.',
                 'Non ancora. Ripassi le lezioni e riprovi.', '尚未通過。請複習單元後再試一次。'),
        'retry': ('Intentarlo otra vez', 'Réessayer', 'Try again', 'Riprova', '再試一次'),
        'review': ('Revise sus respuestas', 'Revoyez vos réponses', 'Review your answers', 'Riveda le sue risposte', '檢視您的答案'),
        'close': ('Cerrar', 'Fermer', 'Close', 'Chiudi', '關閉'),
        'cert': ('Ver mi certificado', 'Voir mon certificat', 'See my certificate', 'Vedi il mio certificato', '查看我的證書'),
        'locked': ('Se habilita cuando haya estudiado todas las lecciones.', 'Disponible quand vous aurez étudié toutes les leçons.', 'Available once you have studied every lesson.',
                   'Disponibile quando avrà studiato tutte le lezioni.', '學完所有單元後即可開始。'),
        'time': ('Tiempo', 'Temps', 'Time', 'Tempo', '時間'),
        'guest': ('Inicie sesión para guardar su resultado y recibir el certificado.', 'Connectez-vous pour enregistrer votre résultat et recevoir le certificat.',
                  'Sign in to save your result and get the certificate.', 'Acceda per salvare il risultato e ricevere il certificato.', '請登入以儲存成績並取得證書。'),
    },
    'progreso': {
        'hello': ('Su aprendizaje', 'Votre apprentissage', 'Your learning', 'Il suo apprendimento', '您的學習'),
        'started': ('cursos iniciados', 'cours commencés', 'courses started', 'corsi iniziati', '門已開始的課程'),
        'seen': ('lecciones estudiadas', 'leçons étudiées', 'lessons studied', 'lezioni studiate', '個已學習單元'),
        'certs': ('certificados', 'certificats', 'certificates', 'certificati', '張證書'),
        'going': ('Continúe donde lo dejó', 'Reprenez là où vous en étiez', 'Pick up where you left off', 'Riprenda da dove era rimasto', '從上次中斷處繼續'),
        'done': ('Completados', 'Terminés', 'Completed', 'Completati', '已完成'),
        'next': ('Cursos sugeridos', 'Cours suggérés', 'Suggested courses', 'Corsi consigliati', '推薦課程'),
        'cont': ('Continuar', 'Continuer', 'Continue', 'Continua', '繼續'),
        'see': ('Ver curso', 'Voir le cours', 'See course', 'Vedi il corso', '查看課程'),
        'cert': ('Certificado', 'Certificat', 'Certificate', 'Certificato', '證書'),
        'empty': ('Todavía no ha empezado ningún curso. Elija uno y empiece por la primera lección.', 'Vous n’avez encore commencé aucun cours. Choisissez-en un et commencez par la première leçon.',
                  'You have not started any course yet. Choose one and begin with the first lesson.', 'Non ha ancora iniziato nessun corso. Ne scelga uno e cominci dalla prima lezione.',
                  '您尚未開始任何課程。請選擇一門課程，從第一個單元開始。'),
        'guest': ('Este progreso está guardado en este dispositivo. Inicie sesión para guardarlo en su cuenta.', 'Cette progression est enregistrée sur cet appareil. Connectez-vous pour la garder dans votre compte.',
                  'This progress is saved on this device. Sign in to keep it in your account.', 'Questo progresso è salvato su questo dispositivo. Acceda per salvarlo nel suo account.',
                  '此進度儲存在此裝置上。請登入以保存到您的帳戶。'),
    },
    'temario': {
        'title': ('Temario del curso', 'Programme du cours', 'Course outline', 'Programma del corso', '課程大綱'),
        'lessons': ('lecciones', 'leçons', 'lessons', 'lezioni', '個單元'),
        'quiz': ('Evaluación final con casos', 'Évaluation finale par études de cas', 'Case-based final assessment', 'Valutazione finale con casi', '個案式期末評量'),
        'video': ('video', 'vidéo', 'video', 'video', '影片'),
    },
}
LANGS = ('fr', 'en', 'it', 'zh-tw')


def words(kind):
    """Ajustes t_* en español para un widget."""
    return {'t_' + k: v[0] for k, v in WORDS[kind].items()}


def merge(path):
    """Copia a traducciones.json las traducciones que falten (no toca las que ya existan)."""
    import json
    tr = json.load(open(path, encoding='utf-8'))
    n = 0
    for kind in WORDS.values():
        for v in kind.values():
            cur = tr.setdefault(v[0], {})
            for ln, x in zip(LANGS, v[1:]):
                if ln not in cur:
                    cur[ln] = x
                    n += 1
    open(path, 'w', encoding='utf-8').write(json.dumps(tr, ensure_ascii=False, indent=1))
    return n


if __name__ == '__main__':
    import os
    print(merge(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'traducciones.json')), 'traducciones añadidas')
