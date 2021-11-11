def input_dirs(entity):
    # hilfiker
    hilf_text_dir = '/mnt/nas2/results/Results/systematicReview/systematicReviews/data/TA_screening/hilfiker_sr_ta/PICO_annotation_project/validation_files/tokens'
    hilf_lab_dir = '/mnt/nas2/results/Results/systematicReview/systematicReviews/data/TA_screening/hilfiker_sr_ta/PICO_annotation_project/validation_files/labels/' + entity + '/annot'

    # EBM-NLP training
    ebm_nlp_text_dir = '/mnt/nas2/results/Results/systematicReview/systematicReviews/data/TA_screening/EBM_NLP/ebm_nlp_2_00/documents/train/'
    ebm_nlp_lab_dir = '/mnt/nas2/results/Results/systematicReview/systematicReviews/data/TA_screening/EBM_NLP/ebm_nlp_2_00/annotations/aggregated/starting_spans/' + entity + '/annot/train/'

    # EBM-NLP Gold
    ebm_gold_text_dir = '/mnt/nas2/results/Results/systematicReview/systematicReviews/data/TA_screening/EBM_NLP/ebm_nlp_2_00/documents/test/'
    ebm_gold_lab_dir = '/mnt/nas2/results/Results/systematicReview/systematicReviews/data/TA_screening/EBM_NLP/ebm_nlp_2_00/annotations/aggregated/starting_spans/' + entity + '/annot/test/gold/'
    
    return [hilf_text_dir, ebm_nlp_text_dir, ebm_gold_text_dir], [hilf_lab_dir, ebm_nlp_lab_dir, ebm_gold_lab_dir]


import os

entity = 'o'

entity_dict = {'p': 'participants', 'i': 'interventions', 'o': 'outcomes'}

# Build sentences from the EBM-NLP dataset
if entity == 'i':
    l1, l2 =[hilf_text_dir, ebm_nlp_text_dir, ebm_gold_text_dir], [hilf_lab_dir, ebm_nlp_lab_dir, ebm_gold_lab_dir] = input_dirs(entity_dict[entity])
elif entity == 'p':
    l1, l2 =[hilf_text_dir, ebm_nlp_text_dir, ebm_gold_text_dir], [hilf_lab_dir, ebm_nlp_lab_dir, ebm_gold_lab_dir] = input_dirs(entity_dict[entity])
elif entity == 'o':
    l1, l2 =[hilf_text_dir, ebm_nlp_text_dir, ebm_gold_text_dir], [hilf_lab_dir, ebm_nlp_lab_dir, ebm_gold_lab_dir] = input_dirs(entity_dict[entity])

    
for txt, lab in zip(l1, l2):
    print('Number of documents: ', len([name for name in os.listdir(txt) if os.path.isfile(os.path.join(txt, name))]))
    print('Number of doc labels: ', len([name for name in os.listdir(lab) if os.path.isfile(os.path.join(lab, name))]))



from nltk.tokenize.punkt import PunktSentenceTokenizer
import nltk, json
import os

write_files = ['/mnt/nas2/data/systematicReview/clinical_trials_gov/Weak_PICO/groundtruth/hilfiker/sentences.txt', '/mnt/nas2/data/systematicReview/clinical_trials_gov/Weak_PICO/groundtruth/ebm_nlp/sentences.txt', '/mnt/nas2/data/systematicReview/clinical_trials_gov/Weak_PICO/groundtruth/ebm_gold/sentences.txt']
#write_files = ['/mnt/nas2/data/systematicReview/clinical_trials_gov/Weak_PICO/groundtruth/hilfiker/sentences.txt']


for n, (token_file, label_file) in enumerate(zip(l1, l2)):
       
    all_text_files = os.listdir(token_file) # token and text files 
    all_lab_files = os.listdir(label_file)
    write_file = write_files[n] # where to write annotations
    
    # Iterate through each text file now
    for i, eachLabFile in enumerate(all_lab_files):
        file2search = eachLabFile.split('.')[0] + '.tokens'
        if '.AGGREGATED.ann' in eachLabFile and file2search in all_text_files:

            document = os.path.join(token_file, file2search)
            label = os.path.join(label_file, eachLabFile)
            
            if os.path.isfile(document) and os.path.isfile(label):
                # collect annotations for each document
                write_document = dict()
                token_list = []
                label_list = []
                
                with open(document, 'r') as doc_file, open(label, 'r') as lab_file:
                    
                    for eachToken, eachTokLabel in zip(doc_file, lab_file):
                        string2print = eachToken.rstrip() + ' : ' + eachTokLabel.rstrip()
                        
                        token_list.append(eachToken.rstrip())
                        label_list.append(eachTokLabel.rstrip())
                        
                        assert len(token_list) == len(label_list)
                        write_document[file2search] = [token_list, label_list]
                    
                #print(write_document)
                
                with open(write_file, 'a+') as wf:
                    json_str = json.dumps(write_document)
                    wf.write(str(json_str))
                    wf.write('\n')
  
    print('---------------------------------------------------------------')