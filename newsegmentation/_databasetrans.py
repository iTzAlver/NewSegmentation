# -------------------------------------------------------------------#
#                                                                    #
#    Author:    Alberto Palomo Alonso.                               #
#                                                                    #
#    Git user:  https://github.com/iTzAlver                          #
#    Email:     ialver.p@gmail.com                                   #
#                                                                    #
# -------------------------------------------------------------------#
import googletrans


def default_dbt(inpath, outpath):
	raw, _, timevector = __get_text(inpath)
	with open(outpath, 'w', encoding='utf-8') as file:
		for line in raw:
			file.writelines(f'{line}\n')
		_text = f'%['
		for time in timevector:
			_text = f'{_text}{time}, '
		lastline = f'{_text[:-2]}]'
		file.writelines(lastline)
	return outpath


def __get_text(route, translate=False, tmodel='google', time_limit='00:05:00'):
	some_text = '!'
	timestamps = ['00:00:00', '00:00:00']
	hover_sliced = ['$ $ $']
	diffs_ = []
	diffs = []
	splitted = ['$$$']
	with open(route, 'r', encoding='utf-8') as file:
		for line in file:
			if line[0:4] == 'NOTE':
				line = next(file)
				if line[0] != '\n':
					return None, None, None
			else:
				if '00:00:00' < line[:] < time_limit:
					timestamps.append([line.split(' --> ')[0][:-4], line.split(' --> ')[1][:8]])
					# diffs_.append(get_diff([line.split(' --> ')[0][:-4], line.split(' --> ')[1][:8]]))
					diffs_.append(get_diff_f([line.split(' --> ')[0], line.split(' --> ')[1][:12]]))
					if timestamps[-1][0] > timestamps[-2][1] and (len(diffs_) == 1 or some_text[-1] == '!'):
						sliced = f'${next(file)}'
					else:
						sliced = next(file)
					while sliced != "\n":
						if _eliminate_buffer(hover_sliced, sliced):
							some_text = f'{some_text} {sliced[:-1]}'
							hover_sliced.append(sliced)
							if '.\n' in hover_sliced[-1]:
								diffs.append(sum(diffs_))
								splitted.append(some_text)
								some_text = ' '
								diffs_ = []
						sliced = next(file)

	splitted = [mutable[2:-1].replace('  ', ' ') for mutable in splitted][1:]

	if translate:
		traduction_splt = _translate(splitted, model=tmodel)
	else:
		traduction_splt = ['No translated.']

	if not len(splitted) == len(traduction_splt):
		print(
			f'Length of traduction is not the same as original: {len(splitted)} != {len(traduction_splt)} '
			f'for route: {route}')

	return [splitted, traduction_splt, diffs]


def get_diff_f(tstamps):
	st0 = tstamps[0].split('.')[0]
	st1 = tstamps[1].split('.')[0]
	dec0 = int(tstamps[0].split('.')[1])
	dec1 = int(tstamps[1].split('.')[1])
	decimal = get_diff([st0, st1])
	ret = round(decimal + (dec1-dec0)/1000, 2)
	return ret


def get_diff(tstamps):
	spt0 = tstamps[0].split(':')
	spt1 = tstamps[1].split(':')
	diff = 0
	for i, diffed in enumerate(spt0):
		diff += (60**(2-i))*(int(spt1[i]) - int(diffed))
	return diff


def _eliminate_buffer(hover_sliced, sliced):
	add_permission = True
	for hover in hover_sliced:
		if sliced == hover:
			add_permission = False
	return add_permission


def _translate(_texts_original, model='google'):
	retext_ = ''
	try:
		_text = []
		dkt = []
		cnt = 0
		for _text_original in _texts_original:
			[_text_, dkt_, cnt] = capital_replace(_text_original, cnt)
			dkt.extend(dkt_)
			_text.append(_text_)
	except Exception as exc:
		print(f'{exc}')
		raise

	if model == 'google':
		g_translator = googletrans.Translator(service_urls=['translate.google.com'])
		if _text is None:
			print('Oops, there was an error translating...')
		else:
			try:
				txt = '\n'.join(_text)
				retext_ = g_translator.translate(txt, src='es').text
				retext_ = retext_.replace('​​', '')
			except Exception as ex:
				print(f'Traceback: VttReading/__translate: Cannot translate \'{_text}\' '
				      f'from model {model}; maybe too many requests.\n{ex}')
	else:
		print(f'Traceback: VttReading/__translate: No translator model called {model}.')
	_retext = capital_restore(retext_, dkt)
	return _retext.split('\n')


def capital_replace(_text, cnt=0):
	unchain_words = []
	ret_phrase = []
	counter = cnt
	iterator_text = _text.split('. ')
	for _text_m in iterator_text:
		chain_words = []
		segmented_text = _text_m.split(' ')
		for idx, word in enumerate(segmented_text):
			if word != '':
				if word[0].isupper() and idx != 0:
					chain_words.append(f'__{counter}__')
					counter += 1
					unchain_words.append(word)
				else:
					chain_words.append(word)
		ret_phrase.append(' '.join(chain_words))
	ret_phrase = '. '.join(ret_phrase)
	return [ret_phrase, unchain_words, counter]


def capital_restore(_text, dkt):
	_text_p = _text
	for idx, word in enumerate(dkt):
		_text_p = _text_p.replace(f'__{idx}__', word)
	return _text_p
# -------------------------------------------------------------------#
#           E   N   D          O   F           F   I   L   E         #
# -------------------------------------------------------------------#
