from distutils.dir_util import copy_tree
import argparse
import git
import glob
import os
import shutil
import sys
import traceback
import zipfile

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', required=True,
                        metavar='repository path', help='repository path')
    parser.add_argument('--zip', required=True,
                        metavar='zip path', help='zip file that downloaded from replit')
    parser.add_argument('--pattern', required=False,
                        metavar='pattern',
						help='file name patterns to extract specific file. multiple patterns can be used by separating commas. eg)test/*,*.md')
    parser.add_argument('--remote', required=False,
                        metavar='remote',
						default='origin',
						help='remote name. default is origin')
    return parser.parse_args()

def validate_or_exit_args(args):
	if os.path.exists(args.repo) == False:
		print(f'No such file or directory: {args.repo}')
		sys.exit()

	if os.path.exists(args.zip) == False:
		print(f'No such file or directory: {args.zip}')
		sys.exit()

def get_filename(path):
	return os.path.splitext(os.path.basename(path))[0]


def extract_zip_to_tmp(path):
	extract_dir = f'./tmp/{get_filename(path)}'
	with zipfile.ZipFile(path) as f:
		f.extractall(extract_dir)
	return extract_dir


def copy_src_file_to_repo(source_dir, repo_path):
	copy_tree(source_dir, repo_path)

def delete_matched_files(patterns, base_dir):
	for ptn in patterns:
		fileList = glob.glob(f'{base_dir}/{ptn}')
		for f in fileList:
			os.remove(f)

def main():
	args = parse_arguments()
	validate_or_exit_args(args)

	print(args.repo)
	feature_branch = get_filename(args.zip)
	repo = git.Repo(args.repo)
	main_branch = repo.active_branch
	try:
		repo.git.checkout('-b', feature_branch)
		print(f'  new branch: {feature_branch}')

		source_dir = extract_zip_to_tmp(args.zip)
		if args.pattern != None:
			delete_matched_files(args.pattern.split(','), source_dir)
		copy_src_file_to_repo(source_dir, args.repo)

		repo.git.add(A=True)
		commit_message = f'Add {feature_branch} solution'
		print(f"  commit: '{commit_message}'")
		repo.index.commit(commit_message)

		remote = repo.remotes[args.remote]
		print(f'  push : {feature_branch} -> {remote.url}')
		remote.push(feature_branch)
	except:
		repo.git.checkout('.')
		print(f'  git checkout {main_branch}')
		repo.git.checkout(main_branch)
		print(f'  git branch -d {feature_branch}')
		repo.delete_head(feature_branch)
		traceback.print_exc()
	finally:
		repo.git.checkout(main_branch)
		if os.path.exists(source_dir):
			shutil.rmtree(source_dir)

if __name__ == '__main__':
    main()
