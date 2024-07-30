from setuptools import find_packages, setup

package_name = 'lds02rr_to_scan'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mrupnie',
    maintainer_email='mrupnie@github.com',
    description='ROS 2 package to convert Xiaomi LDS02RR LiDAR data to /scan topic',
    license='Apache Licence 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lds02rr_to_scan = lds02rr_to_scan.lds02rr_to_scan:main'
        ],
    },
)
