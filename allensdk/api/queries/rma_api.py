# Copyright 2015 Allen Institute for Brain Science
# This file is part of Allen SDK.
#
# Allen SDK is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Allen SDK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Allen SDK.  If not, see <http://www.gnu.org/licenses/>.

from allensdk.api.api import Api

class RmaApi(Api):
    '''
    See: `RESTful Model Access (RMA) <http://help.brain-map.org/display/api/RESTful+Model+Access+%28RMA%29>`_
    '''
    MODEL='model::'
    PIPE='pipe::'
    SERVICE='service::'
    CRITERIA='rma::criteria'
    INCLUDE='rma::include'
    OPTIONS='rma::options'
    ORDER='order'
    NUM_ROWS='num_rows'
    ALL='all'
    START_ROW='start_row'
    COUNT='count'
    ONLY='only'
    EXCEPT='except'
    TABULAR='tabular'
    DEBUG='debug'
    PREVIEW='preview'
    TRUE='true'
    FALSE='false'
    IS='$is'
    EQ='$eq'
    
    def __init__(self, base_uri=None):
        super(RmaApi, self).__init__(base_uri)
    
    
    def build_query_url(self,
                        stage_clauses,
                        fmt='json'):
        '''Combine one or more RMA query stages into a single RMA query.
        
        Parameters
        ----------
        stage_clauses : list of strings
            subqueries
        fmt : string, optional
            json (default), xml, or csv
            
        Returns
        -------
        string
            complete RMA url
        '''
        if not type(stage_clauses) is list:
            stage_clauses = [stage_clauses]
        
        url = ''.join([
            self.rma_endpoint,
            '/query.',
            fmt,
            '?q=',
            ','.join(stage_clauses)])
        
        return url
    
    def model_stage(self,
                    model,
                    **kwargs):
        '''Construct a model stage of an RMA query string.
        
        Parameters
        ----------
        model : string
            The top level data type
        filters : dict
            key, value comparisons applied to the top-level model to narrow the results.            
        criteria : string
            raw RMA criteria clause to choose what object are returned
        include : string
            raw RMA include clause to return associated objects
        only : list of strings, optional
            to be joined into an rma::options only filter to limit what data is returned
        except : list of strings, optional
            to be joined into an rma::options except filter to limit what data is returned            
        tabular : list of string, optional
            return columns as a tabular data structure rather than a nested tree.                    
        count : boolean, optional
            False to skip the extra database count query.                    
        debug : string, optional
            'true', 'false' or 'preview'
        num_rows : int or string, optional
            how many database rows are returned (may not correspond directly to JSON tree structure) 
        start_row : int or string, optional
            which database row is start of returned data  (may not correspond directly to JSON tree structure)
        
        
        Notes
        -----
        See `RMA Path Syntax <http://help.brain-map.org/display/api/RMA+Path+Syntax#RMAPathSyntax-DoubleColonforAxis>`_
        for a brief overview of the normalized RMA syntax.
        Normalized RMA syntax differs from the legacy syntax
        used in much of the RMA documentation.
        Using the &debug=true option with an RMA URL will include debugging information in the
        response, including the normalized query.
        '''
        clauses = [RmaApi.MODEL + model]
        
        filters = kwargs.get('filters', None)
        
        if filters != None:
            clauses.append(self.filters(filters))
            
        criteria = kwargs.get('criteria', None)
        
        if criteria != None:
            clauses.append(',')
            clauses.append(RmaApi.CRITERIA)
            clauses.append(',')
            clauses.extend(criteria)
        
        include = kwargs.get('include', None)
        
        if include != None:
            clauses.append(',')
            clauses.append(RmaApi.INCLUDE)
            clauses.append(',')
            clauses.extend(include)
        
        options_clause = self.options_clause(**kwargs)
        
        if options_clause != '':
            clauses.append(',')
            clauses.append(options_clause)
        
        stage = ''.join(clauses)
        
        return stage
    
    
    def pipe_stage(self,
                   pipe_name,
                   parameters):
        '''Connect model and service stages via their JSON responses.
        
        Notes
        -----
        See: `Service Pipelines <http://help.brain-map.org/display/api/Service+Pipelines>`_ 
        and
        `Connected Services and Pipes <http://help.brain-map.org/display/api/Connected+Services+and+Pipes>`_
        '''
        clauses = [RmaApi.PIPE + pipe_name]
        
        clauses.append(self.tuple_filters(parameters))
        
        stage = ''.join(clauses)
        
        return stage
    
    
    def service_stage(self,
                      service_name,
                      parameters=None):
        '''Construct an RMA query fragment to send a request to a connected service.
        
        Parameters
        ----------
        service_name : string
            Name of a documented connected service.
        parameters : dict
            key-value pairs as in the online documentation.
        
        Notes
        -----
        See: `Service Pipelines <http://help.brain-map.org/display/api/Service+Pipelines>`_ 
        and
        `Connected Services and Pipes <http://help.brain-map.org/display/api/Connected+Services+and+Pipes>`_
        '''
        clauses = [RmaApi.SERVICE + service_name]
        
        if parameters != None:
            clauses.append(self.tuple_filters(parameters))
        
        stage = ''.join(clauses)

        return stage


    def model_query(self, *args, **kwargs):
        '''Construct and execute a model stage of an RMA query string.
        
        Parameters
        ----------
        model : string
            The top level data type
        filters : dict
            key, value comparisons applied to the top-level model to narrow the results.            
        criteria : string
            raw RMA criteria clause to choose what object are returned
        include : string
            raw RMA include clause to return associated objects
        only : list of strings, optional
            to be joined into an rma::options only filter to limit what data is returned
        except : list of strings, optional
            to be joined into an rma::options except filter to limit what data is returned            
        tabular : list of string, optional
            return columns as a tabular data structure rather than a nested tree.                    
        count : boolean, optional
            False to skip the extra database count query.                    
        debug : string, optional
            'true', 'false' or 'preview'
        num_rows : int or string, optional
            how many database rows are returned (may not correspond directly to JSON tree structure) 
        start_row : int or string, optional
            which database row is start of returned data  (may not correspond directly to JSON tree structure)
        
        
        Notes
        -----
        See `RMA Path Syntax <http://help.brain-map.org/display/api/RMA+Path+Syntax#RMAPathSyntax-DoubleColonforAxis>`_
        for a brief overview of the normalized RMA syntax.
        Normalized RMA syntax differs from the legacy syntax
        used in much of the RMA documentation.
        Using the &debug=true option with an RMA URL will include debugging information in the
        response, including the normalized query.
        '''
        return self.json_msg_query(
            self.build_query_url(
                self.model_stage(*args, **kwargs)))
    
    
    def service_query(self, *args, **kwargs):
        '''Construct and Execute a single-stage RMA query
        to send a request to a connected service.
        
        Parameters
        ----------
        service_name : string
            Name of a documented connected service.
        parameters : dict
            key-value pairs as in the online documentation.
        
        Notes
        -----
        See: `Service Pipelines <http://help.brain-map.org/display/api/Service+Pipelines>`_ 
        and
        `Connected Services and Pipes <http://help.brain-map.org/display/api/Connected+Services+and+Pipes>`_
        '''        
        return self.json_msg_query(
            self.build_query_url(
                self.service_stage(*args, **kwargs)))
    
    
    def options_clause(self, **kwargs):
        '''build rma:: options clause.
        
        Parameters
        ----------
        only : list of strings, optional
        except : list of strings, optional
        tabular : list of string, optional
        count : boolean, optional
        debug : string, optional
            'true', 'false' or 'preview'
        num_rows : int or string, optional
        start_row : int or string, optional
        '''
        clause = ''
        options_params = []
        
        only = kwargs.get(RmaApi.ONLY, None)
        
        if only != None:
            options_params.append(
                self.only_except_tabular_clause(RmaApi.ONLY,
                                                only))
        
        excpt = kwargs.get(RmaApi.EXCEPT, None)
        
        if excpt != None:
            options_params.append(
                self.only_except_tabular_clause(RmaApi.EXCEPT,
                                                excpt))
        
        tabular = kwargs.get(RmaApi.TABULAR, None)
        
        if tabular != None:
            options_params.append(
                self.only_except_tabular_clause(RmaApi.TABULAR,
                                                tabular))
        
        num_rows = kwargs.get(RmaApi.NUM_ROWS, None)
        
        if num_rows != None:
            if num_rows == RmaApi.ALL:
                options_params.append("[%s$eq'all']" % (RmaApi.NUM_ROWS))
            else:
                options_params.append('[%s$eq%d]' % (RmaApi.NUM_ROWS,
                                                     num_rows))
        
        start_row = kwargs.get(RmaApi.START_ROW, None)
        
        if start_row != None:
            options_params.append('[%s$eq%d]' % (RmaApi.START_ROW,
                                                 start_row))
        
        order = kwargs.get(RmaApi.ORDER, None)
        
        if order != None:
            options_params.append(self.order_clause(order))
        
        debug = kwargs.get(RmaApi.DEBUG, None)
        
        if debug != None:
            options_params.append(self.debug_clause(debug))
        
        cnt = kwargs.get(RmaApi.COUNT, None)
        
        if cnt != None:
            if cnt == True or cnt == 'true':
                options_params.append('[%s$eq%s]' % (RmaApi.COUNT,
                                                     RmaApi.TRUE))
            elif cnt == False or cnt == 'false':
                options_params.append('[%s$eq%s]' % (RmaApi.COUNT,
                                                     RmaApi.FALSE))
            else:
                pass
        
        if len(options_params) > 0:
            clause = RmaApi.OPTIONS + ''.join(options_params)
        
        return clause
    
    
    def only_except_tabular_clause(self, filter_type, attribute_list):
        '''Construct a clause to filter which attributes are returned
        for use in an rma::options clause.
        
        Parameters
        ----------
        filter_type : string
            'only', 'except', or 'tabular'
        attribute_list : list of strings
            for example ['acronym', 'products.name', 'structure.id']
        
        Returns
        -------
        clause : string
            The query clause for inclusion in an RMA query URL.
        
        Notes
        -----
        The title of tabular columns can be set by adding '+as+<title>'
        to the attribute.
        The tabular filter type requests a response that is row-oriented
        rather than a nested structure.
        Because of this, the tabular option can mask the lazy query behavior
        of an rma::include clause.
        The tabular option does not mask the inner-join behavior of an rma::include
        clause.
        The tabular filter is required for .csv format RMA requests.
        '''
        clause = ''
        
        if attribute_list != None:
            clause = '[%s$eq%s]' % (filter_type,
                                    ','.join(attribute_list))
        
        return clause
    
    
    def order_clause(self, order_list=None):
        '''Construct a debug clause for use in an rma::options clause.

        Parameters
        ----------
        order_list : list of strings
            for example ['acronym', 'products.name+asc', 'structure.id+desc']
        
        Returns
        -------
        clause : string
            The query clause for inclusion in an RMA query URL.
        
        Notes
        -----
        Optionally adding '+asc' (default) or '+desc' after an attribute
        will change the sort order.
        '''
        clause = ''
        
        if order_list != None:
            clause = '[order$eq%s]' % (','.join(order_list))
        
        return clause
    
    
    def debug_clause(self, debug_value=None):
        '''Construct a debug clause for use in an rma::options clause.
        Parameters
        ----------
        debug_value : string or boolean
            True, False, None (default) or 'preview'
        
        Returns
        -------
        clause : string
            The query clause for inclusion in an RMA query URL.
        
        Notes
        -----
        True will request debugging information in the response.
        False will request no debugging information.
        None will return an empty clause.
        'preview' will request debugging information without the query being run.
         
        '''
        clause = ''
        
        if debug_value == None:
            clause = ''
        if debug_value == True or debug_value == 'true':
            clause = '[debug$eqtrue]'
        elif debug_value == False or debug_value == 'false':
            clause = '[debug$eqfalse]'
        elif debug_value == 'preview':
            clause = "[debug$eq'preview']"
        
        return clause
    
    
    # TODO: deprecate for something that can preserve order
    def filters(self, filters):
        '''serialize RMA query filter clauses.
        
        Parameters
        ----------
        filters : dict
            keys and values for narrowing a query.
        
        Returns
        -------
        string
            filter clause for an RMA query string.
        '''
        filters_builder = []
        
        for (key, value) in filters.items():
            filters_builder.append(self.filter(key, value))
        
        return ''.join(filters_builder)
    
    # TODO: this needs to be more rigorous.
    def tuple_filters(self, filters):
        '''Construct an RMA filter clause.
        
        Notes
        -----
        
        See `RMA Path Syntax - Square Brackets for Filters <http://help.brain-map.org/display/api/RMA+Path+Syntax#RMAPathSyntax-SquareBracketsforFilters>`_ for additional documentation.
        '''
        filters_builder = []
        
        for filt in filters:
            if filt[-1] == None:
                continue
            if len(filt) == 2:
                val = filt[1]
                if type(val) is list:
                    val_array = []
                    for v in val:
                        if type(v) is str:
                            val_array.append(v)
                        else:
                            val_array.append(str(v))
                    val = ','.join(val_array)
                    filters_builder.append("[%s$eq%s]" % (filt[0], val))
                elif type(val) is int:
                    filters_builder.append("[%s$eq%d]" % (filt[0], val))
                elif type(val) is bool:
                    if val:
                        filters_builder.append("[%s$eqtrue]" % (filt[0]))
                    else:
                        filters_builder.append("[%s$eqfalse]" % (filt[0]))
                elif type(val) is str:
                    filters_builder.append("[%s$eq%s]" % (filt[0], filt[1]))
            elif len(filt) == 3:
                filters_builder.append("[%s%s%s]" % (filt[0],
                                                     filt[1],
                                                     str(filt[2])))

        
        return ''.join(filters_builder)
    
    
    def quote_string(self, the_string):
        '''Wrap a clause in single quotes.
        
        Parameters
        ----------
        the_string : string
            a clause to be included in an rma query that needs to be quoted
        
        Returns
        -------
        string
            input wrapped in single quotes
        '''
        return ''.join(["'", the_string, "'"])
    
    
    def filter(self, key, value):
        '''serialize a single RMA query filter clause.
        
        Parameters
        ----------
        key : string
            keys for narrowing a query.
        value : string
            value for narrowing a query.
        
        Returns
        -------
        string
            a single filter clause for an RMA query string.
        '''        
        return "".join(['[',
                        key,
                        RmaApi.EQ,
                        str(value),
                        ']'])
    
    
    def build_schema_query(self,  clazz=None, fmt='json'):
        '''Build the URL that will fetch the data schema.
        
        Parameters
        ----------
        clazz : string, optional
            Name of a specific class or None (default).
        fmt : string, optional
            json (default) or xml
        
        Returns
        -------
        url : string
            The constructed URL
        
        Notes
        -----
        If a class is specified, only the schema information for that class
        will be requested, otherwise the url requests the entire schema.
        '''
        if clazz != None:
            class_clause = '/' + clazz
        else:
            class_clause = ''
        
        url = ''.join([self.rma_endpoint,
                       class_clause,
                       '.',
                       fmt])
        
        return url
    
    
    def get_schema(self, clazz=None):
        '''Retrieve schema information.'''
        schema_data = self.do_query(self.build_schema_query,
                                   self.read_data,
                                   clazz)
        
        return schema_data
