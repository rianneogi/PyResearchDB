// #include <qt/QtCore>
#include <QtGui/qimage.h>
#include <poppler/qt5/poppler-qt5.h>
#include <boost/tokenizer.hpp>
#include <iostream>

void run_api()
{
	std::string s;
	std::cin >> s;

	boost::char_separator<char> sep(" ");
    boost::tokenizer<boost::char_separator<char>> tokens(s, sep);
	for (boost::tokenizer<boost::char_separator<char>>::iterator beg = tokens.begin(); beg != tokens.end(); ++beg)
	{
        std::cout << *beg << "." << std::endl;
    }
}

int main()
{
	run_api();
}