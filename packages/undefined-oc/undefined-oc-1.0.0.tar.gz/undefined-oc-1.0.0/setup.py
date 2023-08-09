from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='undefined-oc',
	version='1.0.0',
	description='undefined: simulates the JavaScript undefined behaviour in ' \
		 		'Python',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/ouroboroscoding/undefined-python',
	project_urls={
		'Source': 'https://github.com/ouroboroscoding/undefined-python',
		'Tracker': 'https://github.com/ouroboroscoding/undefined-python/issues'
	},
	keywords=['javascript', 'undefined'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['undefined'],
	python_requires='>=3.10',
	install_requires=[],
	zip_safe=True
)